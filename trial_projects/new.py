# # # from black_jack import logo
# # # from my_data import data
# # # import random
# # #
# # #
# # #
# # # a=random.choice(data)
# # # print(logo)
# # # # print(a)
# # import turtle
# # from turtle import Turtle, Screen
# # import random
# # import tkinter as TK
# #
# # timmy_the_turtle = Turtle()
# #
# # # timmy_the_turtle.shape("turtle")
# # # timmy_the_turtle.color("purple")
# # # timmy_the_turtle.forward("100")
# # # timmy_the_turtle.penup()
# # # # timmy_the_turtle.left("100")
# # # # timmy_the_turtle.up("100")
# #
# # #
# # # number_of_sides = 5
# #
# # colours = ["red", "green", "yellow", "purple"]
# #
# # # def shapes(number_of_sides):
# # #     timmy_the_turtle.color(random.choice(colours))
# # #     for _ in range(number_of_sides):
# # #         angle = int(360 / number_of_sides)
# # #         timmy_the_turtle.forward(100)
# # #         timmy_the_turtle.right(angle)
# # #
# # #
# # # for number_of_sides in range(2, 20):
# # #     shapes(number_of_sides)
# # #
# # direction = [90, 180, 360, 270, ]
# # # for _ in range(40):
# # #     timmy_the_turtle.pensize(12)
# # #     timmy_the_turtle.forward(30)
# # #     timmy_the_turtle.setheading(random.choice(direction))
# # #     timmy_the_turtle.color(random.choice(colours))
# # turtle.colormode(255)
# #
# #
# # def colours():
# #     r = random.randint(0, 255)
# #     g = random.randint(0, 255)
# #     b = random.randint(0, 255)
# #     colour = (r, g, b)
# #     return colour
# #
# #
# # def rand():
# #     for _ in range(1,200):
# #         timmy_the_turtle.forward(30)
# #         timmy_the_turtle.setheading(random.choice(direction))
# #         timmy_the_turtle.color(colours())
# #
# # rand()
# # screen = Screen()
# # screen.exitonclick()
#
# # import colorgram
# # import turtle
# # import random
# #
# # tim = turtle.Turtle()
# # turtle.colormode(255)
# # colours = []
# # colour = colorgram.extract('images.jpg', 6)
# # for colou in colour:
# #     # colours.append(colou.rgb)
# #     r = colou.rgb.r
# #     g = colou.rgb.g
# #     b = colou.rgb.b
# #     new_colour = (r, g, b)
# #     colours.append(new_colour)
# # for _ in range(100):
# #     tim.dot(20,random.choice(colours))
# #     tim.forward((20))
#
# from turtle import Turtle, Screen
#
# screen = Screen()
# screen.bgcolor("green")
# screen.setup(width=800, height=600)
# screen.tracer(0)
#
# paddle = Turtle()
# paddle.shape('square')
# paddle.color('white')
# paddle.shapesize(stretch_wid=5, stretch_len=1)
# paddle.penup()
# paddle.goto(350, 0)
#
#
# def go_up():
#     new_y = paddle.ycor() + 20
#     paddle.goto(paddle.xcor(), new_y)
#
# def go_down():
#     new_y = paddle.ycor() - 20
#     paddle.goto(paddle.xcor(), new_y)
#
# screen_is_on=True
# while screen_is_on:
#     screen.update()
#
#
# screen.listen()
# screen.onkey(go_up, 'Up')
# screen.onkey(go_down, 'Down')
# screen.exitonclick()

from collections import Counter

corpus = "the quick brown fox jumped over the lazy dog"

def kw_matrix(corpus):
    # Split the corpus into individual words
    words = corpus.split()
    print(words,"AAAAAAAAAAAAAAAAAAAAAAAAAAa")
    # Count the frequency of each word
    word_counts = Counter(words)
    print(word_counts,"????????????????????????????????????????")

    # Create an empty matrix
    matrix = {}


