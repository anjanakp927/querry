# import random
# from my_data import data
#
# # def user_draw():
# #     list = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10]
# #     a = random.choice(list)
# #     return a
# #
# #
# # user_list = []
# # computer_list = []
# #
# #
# # def sums():
# #     for _ in range(2):
# #         user_list.append(user_draw())
# #         computer_list.append(user_draw())
# #
# #
# # sums()
# #
# # print(sum(user_list))
# # print(sum(computer_list))
# logo = '''
#
#
#                .__
# __  _  __ ____ |  |   ____  ____   _____   ____
# \ \/ \/ // __ \|  | _/ ___\/  _ \ /     \_/ __ \
#  \     /\  ___/|  |_\  \__(  <_> )  Y Y  \  ___/
#   \/\_/  \___  >____/\___  >____/|__|_|  /\___  >
#              \/          \/            \/     \/
#
# '''
# print(logo)
# logo2 = ''' ___  ________
# \  \/ /  ___/
#  \   /\___ \
#   \_//____  >
#           \/ '''
#
# # number = random.randint(1, 100)
# # print("WELCOME TO THE NUMBER GUESSING GAME")
# # guess = int(input('enter your guess'))
#
# #
# # def choose_difficulty():
# #     difficulty_level = input('choose the difficulty level "HARD" OR "SIMPLE"')
# #
# #
# # def check_answer(guess, number):
# #     if guess > number:
# #         print('TOO HIGH')
# #     elif guess < number:
# #         print('TOO LOW')
# #     else:
# #         print('HEY YOU WON THE GAME')
# #
#
# account_a = random.choice(data)
# account_b = random.choice(data)
# if account_a == account_b:
#     account_a = random.choice(data)
#
#
# def formate_data(datas):
#     name = datas["name"]
#     description = datas["description"]
#     country = datas["country"]
#     follower_count = datas["follower_count"]
#     print(
#         f'your name is {name} your description is {description} your country is {country} your follower  account is {follower_count}')
#
#
# print(f'A:  {formate_data(account_a)}')
# print(logo2)
# print(f'A:  {formate_data(account_b)}')
# a=0
# while a in range(100):
#     answers = input('WHO HAS MORE FOLLOWERS A OR B ?').lower()
#     a_fllower_count = account_a['follower_count']
#     b_fllower_count = account_b['follower_count']
#     print(a_fllower_count)
#     print(b_fllower_count)
#
#
#     def check_answers(a_fllower_count, b_fllower_count, answers):
#         score = 0
#         if a_fllower_count > b_fllower_count:
#             if answers == 'a':
#                 print("YOU ARE THE WINNER OF THE GUESSING")
#                 score += 1
#                 print(f'your score is {score}')
#             else:
#                 print("YOU ARE THE LOSER OF THE GUESSING")
#                 score -= 1
#                 print(f'your score is {score}')
#
#         if a_fllower_count < b_fllower_count:
#             if answers == 'b':
#                 print("YOU ARE THE WINNER OF THE GUESSING")
#                 score += 1
#                 print(f'your score is {score}')
#             else:
#                 print("YOU ARE THE LOSER OF THE GUESSING")
#                 score -= 1
#                 print(f'your score is {score}')
#
#     def process_coins():
#         total=int(input('how many quarters'))*0.25
#
#
#     check_answers(answers, a_fllower_count, b_fllower_count)
#     game = "true"
#     users_wish = input('do you wanna continue"yes"or"no"?').lower()
#
#

class Question:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer


questions = Question("qwertyu", "False")
questions.question
questions.answer
