# 绘制一个图形，最大半径100，画50次，半径每次递减1，起绘点每次往右移5。
from turtle import Pen

p = Pen()
p.speed(10)
x, y = 0, 0  # 设置起始圆心
d = 100  # 起始圆的半径
for _ in range(50):
    p.up()
    p.setpos(x, y)
    p.down()
    p.circle(d)
    x += 5  # 每次画完一个圆，圆心右移5
    d -= 1  # 半径减小1
p.screen.mainloop()
