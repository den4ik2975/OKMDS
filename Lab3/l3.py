import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
from scipy.integrate import odeint


def EqOfMovement(y, t, M, m, l, r, c, g):
    # y[0,1,2,3] = x,phi,x',phi'
    # dy[0,1,2,3] = x',phi',x'',phi''
    dy = np.zeros_like(y)
    dy[0] = y[2] #тривиальные уравнения вида
    dy[1] = y[3] #dx = x’, dphi = phi’

    delta = (m * g) / c

    a11 = ((M / 2) + m)   # коэффициенты первого уравнения
    a12 = 0
    b1 = m * g * np.cos(y[1]) - c * (y[0] + delta) + m * l * y[3] * y[3]

    a21 = 0  # коэффициенты
    a22 = l          # второго уравнения
    b2 = -g * np.sin(y[1]) - y[3] * (2 * y[2] - r * y[3])

    # решение правилом Крамера
    dy[2] = (b1 * a22 - b2 * a12)/(a11 * a22 - a21 * a12)
    dy[3] = (a11 * b2 - a21 * b1)/(a11 * a22 - a21 * a12)

    return dy


STEPS = 1500
START_VALUE = 0
END_VALUE = 6 * np.pi
M = 1
m = 10
r = 0.4
l = 1
c = 50
g = 9.81

x0 = 0.02
phi0 = np.pi / 6
dx0 = 0
dphi0 = 0
y0 = [x0, phi0, dx0, dphi0]

t = np.linspace(START_VALUE, END_VALUE, STEPS) # Сетка по времени

Y = odeint(EqOfMovement, y0, t, (M,m,l,r,c,g))
y = Y[:, 0]
phi = Y[:, 1]
dx = Y[:, 2]
dphi = Y[:, 3]


dY = EqOfMovement(Y, t, M, m, l, r, c, g)
ddx = dY[:, 2]
ddphi = dY[:, 3]

l = l + y - r * phi
dl = dx - r * dphi

N_eps = -m * (l * ddphi + r * dphi * dphi + 2 * dl * dphi) * np.cos(phi) - m * (ddx - l * dphi * dphi) * np.sin(phi)
N_nu = -m * (l * ddphi + r * dphi * dphi + 2 * dl * dphi) * np.sin(phi) + m * (ddx - l * dphi * dphi) * np.cos(phi) - c * y - (M + m) * g

fgr = plot.figure()
gr = fgr.add_subplot(1, 1, 1)
gr.axis('equal')  # устанавливаем одинаковый масштаб по осям

# 2. Задаем основные параметры
XO = 3  # x-координата центра блока
YO = 4  # y-координата центра блока
RB = 0.65  # радиус блока
Y0 = 2.3  # длина
RS = 0.1  # радиус малого круга
NP = 20  # количество витков пружины


# 4. Рисуем неподвижные части механизма
gr.plot([2, 4], [0, 0], 'black', linewidth=3)  # нижняя опора
gr.plot([2, 4], [YO + 0.7, YO + 0.7], 'black', linewidth=3)  # верхняя опора
gr.plot([XO - 0.1, XO, XO + 0.1], [YO + 0.7, YO, YO + 0.7], 'black')  # крепление

# 5. Расчет координат для движущихся частей
y_l = y + Y0  # левая часть механизма
y_r = y - Y0  # правая часть механизма

# Координаты точек механизма
Xb = XO - RB  # x-координата точки B
Yb = YO      # y-координата точки B

# Координаты точки A (движущаяся точка)
Xa = Xb + y_l * np.sin(phi)
Ya = Yb - y_l * np.cos(phi)

# 6. Создаем начальные элементы анимации
AB = gr.plot([Xa[0], Xb], [Ya[0], Yb], 'green')[0]  # стержень AB
L = gr.plot([XO + RB, XO + RB], [YO, YO + y_r[0]], 'green')[0]  # вертикальный стержень

# 7. Создаем круг
Alp = np.linspace(0, 2*np.pi, 100)  # углы для построения окружности
Xc = np.cos(Alp)  # x-координаты точек окружности
Yc = np.sin(Alp)  # y-координаты точек окружности

# Рисуем блок и малый круг
Block = gr.plot(XO + RB * Xc, YO + RB * Yc, 'black')[0]  # основной блок
m = gr.plot(Xa[0] + RS * Xc, Ya[0] + RS * Yc, 'black')[0]  # малый круг

# Создаем пружину
Yp = np.linspace(0, 1, 2 * NP + 1)  # y-координаты точек пружины
Xp = 0.15 * np.sin(np.pi/2*np.arange(2 * NP + 1))  # x-координаты точек пружины
Pruzh = gr.plot(XO + RB + Xp, (YO + y_r[0]) * Yp)[0]  # рисуем пружину


# 8. Функция обновления кадров анимации
def run(i):
    # Обновляем положения всех движущихся элементов
    m.set_data([Xa[i] + RS * Xc], [Ya[i] + RS * Yc])  # движение малого круга
    AB.set_data([Xa[i], Xb], [Ya[i], Yb])  # движение стержня AB
    L.set_data([XO + RB, XO + RB], [YO, YO + y_r[i]])  # движение вертикального стержня
    Pruzh.set_data(XO + RB + Xp, (YO + y_r[i]) * Yp)  # движение пружины

    return [m, AB, Block, Pruzh]

# 9. Создаем анимацию
anim = FuncAnimation(fgr, run, frames=STEPS, interval=1)  # interval=1 задает скорость анимации

# Показываем результат
plot.show()