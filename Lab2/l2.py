# 0. Импортируем необходимые библиотеки
import math
import numpy as np  # numpy для математических вычислений
import matplotlib.pyplot as plot  # для создания графиков
from matplotlib.animation import FuncAnimation  # для анимации

# 1. Создаем фигуру и оси для графика
fgr = plot.figure()
gr = fgr.add_subplot(1, 1, 1)
gr.axis('equal')  # устанавливаем одинаковый масштаб по осям

# 2. Задаем основные параметры
STEPS = 500
START_VALUE = 0
END_VALUE = 2 * math.pi
XO = 3  # x-координата центра блока
YO = 4  # y-координата центра блока
RB = 0.5  # радиус блока
Y0 = 2.3  # длина
RS = 0.1  # радиус малого круга
SA = np.pi/18 # Начальное отклонение
NP = 20  # количество витков пружины

# 3. Создаем временный массив
t = np.linspace(START_VALUE, END_VALUE, STEPS)  # временной массив
y = np.sin(t)  # синусоидальное движение

# 4. Рисуем неподвижные части механизма
gr.plot([2, 4], [0, 0], 'black', linewidth=3)  # нижняя опора
gr.plot([2, 4], [YO + 0.7, YO + 0.7], 'black', linewidth=3)  # верхняя опора
gr.plot([XO - 0.1, XO, XO + 0.1], [YO + 0.7, YO, YO + 0.7], 'black')  # крепление

# 5. Расчет координат для движущихся частей
y_l = y + Y0  # левая часть механизма
y_r = y - Y0  # правая часть механизма
phi = SA * np.sin(2*t)  # угол поворота. 2t так как груз совершает два полных колебания

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
