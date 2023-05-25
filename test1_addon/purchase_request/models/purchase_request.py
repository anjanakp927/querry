from odoo import _, api, fields, models
from odoo.exceptions import UserError

_STATES = [
    ("draft", "Draft"),
    ("to_approve", "Confirmed"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("done", "Done"),
]


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _description = "Purchase Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    hms_purchase_req_id = fields.Char(string='HMS PURCHASE REQ ID')
    _sql_constraints = [
        ('hms_purchase_req_id_unique', 'unique(hms_purchase_req_id)', _(" ID already exist!")),
    ]

    @api.model
    def _company_get(self):
        return self.env["res.company"].browse(self.env.company.id)

    @api.model
    def _get_default_requested_by(self):
        return self.env["res.users"].browse(self.env.uid)


    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("to_approve", "approved", "rejected", "done"):
                rec.is_editable = False
            else:
                rec.is_editable = True

    @api.depends("line_ids", "line_ids.estimated_cost")
    def _compute_is_create_po(self):
        min_rfq_count = int(self.env['ir.config_parameter'].sudo().get_param(
            'purchase_requests.min_rfq_count'))

        min_amount = self.company_id.po_double_validation_amount
        print(f".....min  {min_rfq_count} type of {type(min_rfq_count)}")
        print(f".....min amount {min_amount} type of {type(min_amount)}")
        total_amount = 0
        for rec in self:
            for line in rec.line_ids:
                total_amount += line.estimated_cost
            if (total_amount > min_amount) and rec.rfq_count < min_rfq_count:
                rec.is_create_po = False
            else:
                rec.is_create_po = True

    name = fields.Char(
        string="Request Reference",
        track_visibility="onchange",
        default='New'
    )
    # picking_type_id = fields.Many2one(
    #     'stock.picking.type', 'Operation Type',
    #     required=True
    #     )
    origin = fields.Char(string="Source Document")
    date_start = fields.Date(
        string="Creation date",
        help="Date when the user initiated the request.",
        default=fields.Date.context_today,
        track_visibility="onchange",
    )
    requested_by = fields.Many2one(
        comodel_name="res.users",
        string="Requested by",
        required=True,
        copy=False,
        track_visibility="onchange",
        default=_get_default_requested_by,
        index=True,
    )

    assigned_to = fields.Many2one(
        comodel_name="res.users",
        string="Approver",
        track_visibility="onchange",
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("purchase_request.group_purchase_request_manager").id,
            )
        ],
        index=True,
    )
    description = fields.Text(string="Description")
    reason = fields.Text(string="Reason")
    remarks = fields.Text(string="Remarks")
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        required=True,
        default=_company_get,
        track_visibility="onchange",
    )
    line_ids = fields.One2many(
        comodel_name="purchase.request.line",
        inverse_name="request_id",
        string="Products to Purchase",
        readonly=False,
        copy=True,
        track_visibility="onchange",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        related="line_ids.product_id",
        string="Product",
        readonly=True,
    )
    state = fields.Selection(
        selection=_STATES,
        string="Status",
        index=True,
        track_visibility="onchange",
        required=True,
        copy=False,
        default="draft",
    )
    is_editable = fields.Boolean(
        string="Is editable", compute="_compute_is_editable", readonly=True
    )
    to_approve_allowed = fields.Boolean(compute="_compute_to_approve_allowed")

    line_count = fields.Integer(
        string="Purchase Request Line count",
        compute="_compute_line_count",
        readonly=True,
    )
    purchase_ids = fields.One2many('purchase.order', 'request_id', string="Purchase Orders")
    rfq_ids = fields.One2many('purchase.quotation', 'request_id', string="Purchase Quotations")

    purchase_count = fields.Integer(
        string="Purchases count", compute="_compute_purchase_count", readonly=True
    )
    rfq_count = fields.Integer(
        string="Quotations count", compute="_compute_quotation_count", readonly=True
    )
    is_create_po = fields.Boolean(
        string="Create PO", compute="_compute_is_create_po", readonly=True
    )

    part_no = fields.Char('Part Number', related='product_id.part_number', readonly=True)
    requesition_mode = fields.Selection('Requisition Mode', related='product_id.purchase_authority', readonly=True)


    @api.depends("purchase_ids")
    def _compute_purchase_count(self):
        for rec in self:
            rec.purchase_count = len(rec.mapped("purchase_ids"))

    @api.depends("rfq_ids")
    def _compute_quotation_count(self):
        for rec in self:
            rec.rfq_count = len(rec.mapped("rfq_ids"))

    def action_create_quotation(self):
        quotation = self.env['purchase.quotation'].create({
            # 'partner_id': self.partner_id.id,
            'quotation_id': self.id,
            'state': 'purchase',
            'origin': self.name,
            # 'date_order': fields.Datetime.now()
        })
        for line in self.line_ids:
            self.env['purchase.quotation.line'].create({
                'quotation_id': quotation.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'price_unit': line.estimated_cost,
                # 'taxes_id': [(6, 0, line.taxes_id.ids)],

            })


    def action_view_purchase_order(self):
        action = self.env.ref("purchase.purchase_form_action").read()[0]
        lines = self.mapped("purchase_ids")
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [
                (self.env.ref("purchase.purchase_order_form").id, "form")
            ]
            action["res_id"] = lines.id
        return action

    def action_view_rfq(self):
        # action = self.env.ref('purchase_quotations.purchase_rfq').read()[0](original code error)
        action = self.env.ref('purchase_quotations.purchase_rfq_form_action').read()[0]

        lines = self.mapped("rfq_ids")
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action['views'] = [(self.env.ref('purchase_quotations.purchase_quotation_form').id, 'form')]
            action["res_id"] = lines.id
        return action

    @api.depends("line_ids")
    def _compute_line_count(self):
        for rec in self:
            rec.line_count = len(rec.mapped("line_ids"))

    def action_view_purchase_request_line(self):
        action = self.env.ref(
            "purchase_request.purchase_request_line_form_action"
        ).read()[0]
        lines = self.mapped("line_ids")
        if len(lines) > 1:
            action["domain"] = [("id", "in", lines.ids)]
        elif lines:
            action["views"] = [
                (self.env.ref("purchase_request.purchase_request_line_form").id, "form")
            ]
            action["res_id"] = lines.ids[0]
        return action

    @api.depends("state", "line_ids.product_qty", "line_ids.cancelled")
    def _compute_to_approve_allowed(self):
        for rec in self:
            rec.to_approve_allowed = rec.state == "draft" and any(
                not line.cancelled and line.product_qty for line in rec.line_ids
            )

    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({"state": "draft", "name": self._get_default_name()})
        return super(PurchaseRequest, self).copy(default)

    @api.model
    def _get_partner_id(self, request):
        user_id = request.assigned_to or self.env.user
        return user_id.partner_id.id

    @api.model
    def create(self, vals):
        request = super(PurchaseRequest, self).create(vals)
        if vals.get("assigned_to"):
            partner_id = self._get_partner_id(request)
            request.message_subscribe(partner_ids=[partner_id])
        return request

    def write(self, vals):
        res = super(PurchaseRequest, self).write(vals)
        for request in self:
            if vals.get("assigned_to"):
                partner_id = self._get_partner_id(request)
                request.message_subscribe(partner_ids=[partner_id])
        return res

    def _can_be_deleted(self):
        self.ensure_one()
        return self.state == "draft"

    def unlink(self):
        for request in self:
            if not request._can_be_deleted():
                raise UserError(
                    _("You cannot delete a purchase request which is not draft.")
                )
        return super(PurchaseRequest, self).unlink()

    def button_draft(self):
        self.mapped("line_ids").do_uncancel()
        return self.write({"state": "draft"})

    def button_to_approve(self):
        self.to_approve_allowed_check()
        self.name = self.env["ir.sequence"].next_by_code("purchase.request")
        return self.write({"state": "to_approve"})

    def button_approved(self):
        return self.write({"state": "approved"})

    def button_rejected(self):
        self.mapped("line_ids").do_cancel()
        return self.write({"state": "rejected"})

    def button_done(self):
        return self.write({"state": "done"})

    def check_auto_reject(self):
        """When all lines are cancelled the purchase request should be
        auto-rejected."""
        for pr in self:
            if not pr.line_ids.filtered(lambda l: l.cancelled is False):
                pr.write({"state": "rejected"})

    def confirmation(self):
        self.write({'state': 'confirmed'})

    def to_approve_allowed_check(self):
        for rec in self:
            if not rec.to_approve_allowed:
                raise UserError(
                    _(
                        "You can't request an approval for a purchase request "
                        "which is empty lines."
                    )
                )
