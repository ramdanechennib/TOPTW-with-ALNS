import turtle

# Initialize the screen and turtle
screen = turtle.Screen()
screen.bgcolor("skyblue")
t = turtle.Turtle()
t.speed(2)
t.pensize(2)

# Draw the main rectangle (building facade)
t.penup()
t.goto(-150, -100)  # Starting position
t.pendown()
t.color("grey")
t.begin_fill()
t.forward(300)  # Width
t.left(90)
t.forward(200)  # Height
t.left(90)
t.forward(300)
t.left(90)
t.forward(200)
t.left(90)
t.end_fill()

# Draw the door (if present)
t.penup()
t.goto(-30, -100)
t.pendown()
t.color("brown")
t.begin_fill()
t.forward(60)  # Door width
t.left(90)
t.forward(90)  # Door height
t.left(90)
t.forward(60)
t.left(90)
t.forward(90)
t.left(90)
t.end_fill()

# Draw windows (if present)
# Left window
t.penup()
t.goto(-100, 0)
t.pendown()
t.color("white")
t.begin_fill()
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.end_fill()

# Right window
t.penup()
t.goto(50, 0)
t.pendown()
t.begin_fill()
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.forward(50)
t.left(90)
t.end_fill()

# Draw roof (if present)
t.penup()
t.goto(-150, 100)
t.pendown()
t.color("darkred")
t.begin_fill()
t.left(30)
t.forward(173)
t.left(120)
t.forward(173)
t.end_fill()

# Complete drawing
t.hideturtle()
screen.mainloop()

