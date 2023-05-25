# data = [{'name': 'aarya',
#          'follower_count': '345',
#          'description': 'social media plateform',
#          'country': 'united states', },
#         {'name': 'ammu',
#          'follower_count': '292',
#          'description': 'football',
#          'country': 'bangalor', },
#         {'name': 'annu',
#          'follower_count': '443',
#          'description': 'singer',
#          'country': 'oman', },
#         {'name': 'dev',
#          'follower_count': '4343',
#          'description': 'dancer',
#          'country': 'quator', }, ]
# menu = {'expresso': {
#     'ingredients': {
#         'water': 200,
#         'coffee': 24,
#     },
#     "cost": 56,
# },
#
#     'latte': {
#         'ingredients': {
#             'water': 250,
#             'coffee': 24,
#         },
#         "cost": 56,
#     },
#     'cappuccino': {
#         'ingredients': {
#             'water': 200,
#             'coffee': 24,
#         },
#         "cost": 56,
#     },
# }
# resources = {
#     'water': 300,
#     'milk': 200,
#     'cofee': 100,
# }
#
#
# def is_resources_sufficient(ingredients):
#     for item in order_ingredient:
#         if order_ingredient[item] >= resources[item]:
#             print("there is no enough water")
#             return False
#         return True
#
#
#
# is_on = True
# while is_on:
#     a = input("what would u like to have?,coffee/latte/cappuccino")
#     if a == "off":
#         is_on = False
#     elif a == "report":
#         print(f"water:{resources['water']}ml")
#         print(f"water:{resources['milk']}ml")
#         print(f"water:{resources['coffee']}ml")
#     else:
#         drink = menu["a"]
#         print(drink)
#         order_ingredient = is_resources_sufficient(drink["ingredients"])
question_data = [{"text": "A slug's blood is green.", "answer": "True"},
                 {"text": "The loudest animal is the African Elephant.", "answer": "False"},
                 {"text": "Approximately one quarter of human bones are in the feet.", "answer": "True"},
                 {"text": "The total surface area of a human lungs is the size of a football pitch.", "answer": "True"},
                 {
                     "text": "In West Virginia, USA, "
                           "if you accidentally hit an animal with your car, you are free to take it home to eat.",
                     "answer": "True"},
                 {
                     "text": "In London, UK, if you happen to die in the House of Parliament, you are entitled to a state funeral.",
                     "answer": "False"},
                 {"text": "It is illegal to pee in the Ocean in Portugal.", "answer": "True"},
                 {"text": "You can lead a cow down stairs but not up stairs.", "answer": "False"},
                 {"text": "Google was originally called 'Backrub'.", "answer": "True"},
                 {"text": "Buzz Aldrin's mother's maiden name was 'Moon'.", "answer": "True"},
                 {"text": "No piece of square dry paper can be folded in half more than 7 times.", "answer": "False"},
                 {"text": "A few ounces of chocolate can to kill a small dog.", "answer": "True"}
                 ]
