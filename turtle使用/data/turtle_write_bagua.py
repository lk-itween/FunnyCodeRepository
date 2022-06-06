import turtle as t

# 设置背景和笔的移动速度及大小
t.bgcolor('yellow')
t.speed(10)
t.pensize(6)

# 画黑色的半圆
t.fillcolor("black")
t.begin_fill()
t.circle(100,180)
t.left(0)
t.circle(50,180)
t.circle(-50,180)
t.end_fill()

# 画白色的半圆
t.fillcolor("white")
t.begin_fill()
t.circle(-100,180)
t.left(180)
t.circle(50,180)
t.circle(-50,180)
t.end_fill()

# 在黑圆画白色的点
t.left(180)
t.up()
t.goto(10,150)
t.down()
t.pencolor("white")
t.fillcolor("white")
t.begin_fill()
t.circle(13)
t.end_fill()

# 在白圆画黑色的点
t.up()
t.goto(-10,30)
t.fillcolor("black")
t.begin_fill()
t.circle(15)
t.end_fill()
t.pencolor('blue')
t.goto(1000,1000)
t.done()
