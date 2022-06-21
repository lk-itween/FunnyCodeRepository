# 画出楼梯造型的图案
import turtle as t

t.speed(1)
step = 4  # 楼梯阶数
hight = 30  # 每个台阶的长度

t.left(90)
for _ in range(step):
    t.forward(hight)
    t.right(90)
    t.forward(hight)
    t.left(90)
t.left(180)
t.forward(hight * step)
t.right(90)
t.forward(hight * step)

t.mainloop()
