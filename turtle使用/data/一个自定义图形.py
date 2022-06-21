# 画出以下图形，正方形上方缺失一个以正方形对角线一半作为直角边长的三角形
import turtle as t
import math

t.speed(1)
hight = 120  正方形边长
z = round(math.sqrt(hight ** 2 * 2) / 2, 2)

t.left(45)
t.forward(z)
t.right(135)
# t.forward(hight)
for _ in range(3):
    t.forward(hight)
    t.right(90)
t.right(45)
t.forward(z)
t.mainloop()
