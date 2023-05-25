from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseRequestRfqWizard(models.TransientModel):
    _name = "purchase.request.rfq.wizard"
    _description = "Purchase Request Line Make RFQ"

    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier",
        required=True,
        domain=[("is_company", "=", True)],
        context={"res_partner_search_mode": "supplier", "default_is_company": True},
    )
    item_ids = fields.One2many(
        comodel_name="purchase.request.rfq.line",
        inverse_name="wiz_id",
        string="Items",
    )
    purchase_order_id = fields.Many2one(
        comodel_name="purchase.order",
        string="Purchase Order",
        domain=[("state", "=", "draft")],
    )
    sync_data_planned = fields.Boolean(
        string="Merge on PO lines with equal Scheduled Date"
    )

    @api.model
    def _prepare_item(self, line):
        return {
            "line_id": line.id,
            "request_id": line.request_id.id,
            "product_id": line.product_id.id,
            "name": line.name or line.product_id.name,
            "product_qty": line.product_qty,
            "product_uom_id": line.product_uom_id.id,
        }

    @api.model
    def _check_valid_request_line(self, request_line_ids):
        picking_type = False
        company_id = False

        for line in self.env["purchase.request.line"].browse(request_line_ids):
            if line.request_id.state == "done":
                raise UserError(_("The purchase has already been completed."))
            if line.request_id.state != "approved":
                raise UserError(
                    _("Purchase Request %s is not approved") % line.request_id.name
                )

            if line.purchase_state == "done":
                raise UserError(_("The purchase has already been completed."))

            line_company_id = line.company_id and line.company_id.id or False
            if company_id is not False and line_company_id != company_id:
                raise UserError(_("You have to select lines from the same company."))
            else:
                company_id = line_company_id

            # line_picking_type = line.request_id.picking_type_id or False
            # if not line_picking_type:
            #     raise UserError(_("You have to enter a Picking Type."))
            # if picking_type is not False and line_picking_type != picking_type:
            #     raise UserError(
            #         _("You have to select lines from the same Picking Type.")
            #     )
            # else:
            #     picking_type = line_picking_type

    # @api.model
    # def check_group(self, request_lines):
    #     if len(list(set(request_lines.mapped("request_id.group_id")))) > 1:
    #         raise UserError(
    #             _(
    #                 "You cannot create a single purchase quotation from "
    #                 "purchase requests that have different procurement group."
    #             )
    #         )

    @api.model
    def get_items(self, request_line_ids):
        request_line_obj = self.env["purchase.request.line"]
        items = []
        request_lines = request_line_obj.browse(request_line_ids)
        self._check_valid_request_line(request_line_ids)
        # self.check_group(request_lines)
        for line in request_lines:
            items.append([0, 0, self._prepare_item(line)])
        return items

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        active_model = self.env.context.get("active_model", False)
        request_line_ids = []
        if active_model == "purchase.request.line":
            request_line_ids += self.env.context.get("active_ids", [])
        elif active_model == "purchase.request":
            request_ids = self.env.context.get("active_ids", False)
            request_line_ids += (
                self.env[active_model].browse(request_ids).mapped("line_ids.id")
            )
        if not request_line_ids:
            return res
        res["item_ids"] = self.get_items(request_line_ids)
        request_lines = self.env["purchase.request.line"].browse(request_line_ids)
        supplier_ids = request_lines.mapped("supplier_id").ids
        if len(supplier_ids) == 1:
            res["supplier_id"] = supplier_ids[0]
        return res

    @api.model
    def _prepare_purchase_quotation(self, company, origin):
        if not self.supplier_id:
            raise UserError(_("Enter a supplier."))
        supplier = self.supplier_id
        data = {
            "origin": origin,
            "partner_id": self.supplier_id.id,
            "fiscal_position_id": supplier.property_account_position_id
                                  and supplier.property_account_position_id.id
                                  or False,
            # "picking_type_id": picking_type.id,
            "company_id": company.id,
            # "group_id": group_id.id,
        }
        return data

    @api.model
    def _get_purchase_line_onchange_fields(self):
        return ["product_uom", "price_unit", "name", "taxes_id"]

    @api.model
    def _execute_purchase_line_onchange(self, vals):
        cls = self.env["purchase.request.line"]
        onchanges_dict = {
            "onchange_product_id": self._get_purchase_line_onchange_fields()
        }
        for onchange_method, changed_fields in onchanges_dict.items():
            if any(f not in vals for f in changed_fields):
                obj = cls.new(vals)
                getattr(obj, onchange_method)()
                for field in changed_fields:
                    vals[field] = obj._fields[field].convert_to_write(obj[field], obj)

    def create_allocation(self, po_line, pr_line, new_qty, alloc_uom):
        vals = {
            "requested_product_uom_qty": new_qty,
            "product_uom_id": alloc_uom.id,
            "purchase_request_line_id": pr_line.id,
            "purchase_line_id": po_line.id,
        }
        return self.env["purchase.request.allocation"].create(vals)

    @api.model
    def _prepare_purchase_quotation_line(self, po, item):
        if not item.product_id:
            raise UserError(_("Please select a product for all lines"))
        product = item.product_id

        # Keep the standard product UOM for purchase quotation so we should
        # convert the product quantity to this UOM
        qty = item.product_uom_id._compute_quantity(
            item.product_qty, product.uom_po_id or product.uom_id
        )
        # Suggest the supplier min qty as it's done in Odoo core
        min_qty = item.line_id._get_supplier_min_qty(product, po.partner_id)
        qty = max(qty, min_qty)
        date_required = item.line_id.date_required
        vals = {
            "name": product.name,
            "quotation_id": po.id,
            "product_id": product.id,
            "product_uom": product.uom_po_id.id or product.uom_id.id,
            "price_unit": 0.0,
            "product_qty": qty,
            "account_analytic_id": item.line_id.analytic_account_id.id,
            # "purchase_request_lines": [(4, item.line_id.id)],
            "date_planned": datetime(
                date_required.year, date_required.month, date_required.day
            ),
            # "move_dest_ids": [(4, x.id) for x in item.line_id.move_dest_ids],
        }
        if item.line_id.analytic_tag_ids:
            vals["analytic_tag_ids"] = [
                (4, ati) for ati in item.line_id.analytic_tag_ids.ids
            ]
        # self._execute_purchase_line_onchange(vals)
        return vals

    @api.model
    def _get_purchase_line_name(self, quotation, line):
        product_lang = line.product_id.with_context(
            {"lang": self.supplier_id.lang, "partner_id": self.supplier_id.id}
        )
        name = product_lang.display_name
        if product_lang.description_purchase:
            name += "\n" + product_lang.description_purchase
        return name

    @api.model
    def _get_quotation_line_search_domain(self, quotation, item):
        vals = self._prepare_purchase_quotation_line(quotation, item)
        name = self._get_purchase_line_name(quotation, item)
        quotation_line_data = [
            ("quotation_id", "=", quotation.id),
            ("name", "=", name),
            ("product_id", "=", item.product_id.id or False),
            ("product_uom", "=", vals["product_uom"]),
            ("account_analytic_id", "=", item.line_id.analytic_account_id.id or False),
        ]
        if self.sync_data_planned:
            date_required = item.line_id.date_required
            quotation_line_data += [
                (
                    "date_planned",
                    "=",
                    datetime(
                        date_required.year, date_required.month, date_required.day
                    ),
                )
            ]
        if not item.product_id:
            quotation_line_data.append(("name", "=", item.name))
        return quotation_line_data

    def make_purchase_quotation(self):
        res = []
        purchase_obj = self.env["purchase.quotation"]
        po_line_obj = self.env["purchase.quotation.line"]
        purchase = False
        if not self.supplier_id:
            raise UserError(_("Enter a supplier."))

        for item in self.item_ids:
            line = item.line_id
            if item.product_qty <= 0.0:
                raise UserError(_("Enter a positive quantity."))
            if not purchase:
                po_data = {
                    "origin": line.origin,
                    'request_id': line.request_id.id,
                    "partner_id": self.supplier_id.id,
                    "fiscal_position_id": self.supplier_id.property_account_position_id
                                          and self.supplier_id.property_account_position_id.id or False,
                    "company_id": line.company_id.id,
                }
                purchase = purchase_obj.create(po_data)

            # Allocation UoM has to be the same as PR line UoM
            alloc_uom = line.product_uom_id
            wizard_uom = item.product_uom_id

            po_line_data = self._prepare_purchase_quotation_line(purchase, item)
            if item.keep_description:
                po_line_data["name"] = item.name
            po_line = po_line_obj.create(po_line_data)
            product_uom_qty = wizard_uom._compute_quantity(
                item.product_qty, alloc_uom
            )
            po_line.product_qty = product_uom_qty
            po_line._onchange_quantity()
            # The onchange quantity is altering the scheduled date of the PO
            # lines. We do not want that:
            date_required = item.line_id.date_required
            po_line.date_planned = datetime(
                date_required.year, date_required.month, date_required.day
            )
            res.append(purchase.id)

        return {
            "domain": [("id", "in", res)],
            "name": _("RFQ"),
            "view_mode": "tree,form",
            "res_model": "purchase.quotation",
            "view_id": False,
            "context": False,
            "type": "ir.actions.act_window",
        }


class PurchaseRequestRfqLine(models.TransientModel):
    _name = "purchase.request.rfq.line"
    _description = "Purchase Request Line Make Purchase quotation Item"

    wiz_id = fields.Many2one(
        comodel_name="purchase.request.rfq.wizard",
        string="Wizard",
        required=True,
        ondelete="cascade",
        readonly=True,
    )
    line_id = fields.Many2one(
        comodel_name="purchase.request.line", string="Purchase Request Line"
    )
    request_id = fields.Many2one(
        comodel_name="purchase.request",
        related="line_id.request_id",
        string="Purchase Request",
        readonly=False,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        related="line_id.product_id",
        readonly=False,
    )
    name = fields.Char(string="Description", required=True)
    product_qty = fields.Float(
        string="Quantity to purchase", digits="Product Unit of Measure"
    )
    product_uom_id = fields.Many2one(
        comodel_name="uom.uom", string="UoM", required=True
    )
    keep_description = fields.Boolean(
        string="Copy descriptions to new PO",
        help="Set true if you want to keep the "
             "descriptions provided in the "
             "wizard in the new PO.",
    )

    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            if not self.keep_description:
                name = self.product_id.name
            code = self.product_id.code
            sup_info_id = self.env["product.supplierinfo"].search(
                [
                    "|",
                    ("product_id", "=", self.product_id.id),
                    ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                    ("name", "=", self.wiz_id.supplier_id.id),
                ]
            )
            if sup_info_id:
                p_code = sup_info_id[0].product_code
                p_name = sup_info_id[0].product_name
                name = "[{}] {}".format(
                    p_code if p_code else code, p_name if p_name else name
                )
            else:
                if code:
                    name = "[{}] {}".format(
                        code, self.name if self.keep_description else name
                    )
            if self.product_id.description_purchase and not self.keep_description:
                name += "\n" + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            if name:
                self.name = name
