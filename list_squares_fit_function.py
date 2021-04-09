from math import log
from math import exp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib import use
from random import choice as ch
from random import uniform as uf

def linear_build_a(x, y, n):
    summ1 = 0.0
    summ2 = 0.0
    summ3 = 0.0
    for i in range(n):
        summ1 += x[i] * y[i]
        summ2 += x[i]
        summ3 += y[i]
    chisl = (n * summ1) - (summ2 * summ3)
    summ1 = 0.0
    for i in range(n):
        summ1 += x[i] * x[i]
    znam = (n * summ1) - (summ2 * summ2)
    return chisl / znam

def linear_build_b(x, y, n, a):
    summ1 = 0.0
    summ2 = 0.0
    for i in range(n):
        summ1 += x[i]
        summ2 += y[i]
    return (((1.0 / float(n)) * summ2) - ((a * (1.0 / float(n))) * summ1))

def linear_sum_fault(x,y,a,b):
	summ = 0 
	for i in range(len(x)):
		summ += pow(((a * x[i] + b) - y[i]), 2)
	return summ

def pow_build_a(x, y, n):
    for i in range(n):
        x[i] = log(x[i])
        y[i] = log(y[i])
    return linear_build_a(x, y, n)

def pow_build_peta(x, y, n, a):
    for i in range(n):
        x[i] = log(x[i])
        y[i] = log(y[i])
    return exp(linear_build_b(x, y, n, a))

def pow_sum_fault(x,y,a,peta):
    summ = 0
    for i in range(len(x)):
    	summ += pow((peta * pow(x[i], a) - y[i]), 2)
    return summ

def exp_build_a(x, y, n):
    for i in range(n):
        y[i] = log(y[i])
    return linear_build_a(x, y, n)

def exp_build_peta(x, y, n, a):
    for i in range(n):
        y[i] = log(y[i])
    return exp(linear_build_b(x, y, n, a))

def exp_sum_fault(x,y,a,peta):
    summ = 0
    for i in range(len(x)):
    	summ += pow((peta * exp(a * x[i]) - y[i]), 2)
    return summ

def sum_list(data_list, j=1, log=1):
    if (log == 1):
        sum_l = round(sum([i ** j for i in data_list]), 4)
    else:
        sum_l = round(sum([math.log(i) ** j for i in data_list]), 4)
    return sum_l

def sum_two_list(f_data, s_data, j=1):
    sum_l = round(sum([(i ** j) * s_data[f_data.index(i)] for i in f_data]), 4)
    return sum_l

def determ3(delta):
    a = b = c = ai = bi = ci = 1
    for i in range(0, 3):
        a *= delta[i][i]
        if (i < 2):
            b *= delta[i][i + 1]
        if (i > 0):
            c *= delta[i][i - 1]
        if (i < 2):
            ai *= delta[i][2 - i]
        if (i < 2):
            bi *= delta[i][1 - i]
        if (i > 0):
            ci *= delta[i][3 - i]
    b *= delta[2][0]
    c *= delta[0][2]
    ai *= delta[2][0]
    bi *= delta[2][2]
    ci *= delta[0][0]
    return (a + b + c - ai - bi - ci)

def quad_func(x, y):
    sum_x = sum_list(x)
    sum_y = sum_list(y)
    sum_x_2 = sum_list(x, 2)
    sum_x_3 = sum_list(x, 3)
    sum_x_4 = sum_list(x, 4)
    sum_x_y = sum_two_list(x, y)
    sum_x_2_y = sum_two_list(x, y, 2)
    line = len(x)
    determine = determ3([[sum_x_4, sum_x_3, sum_x_2], [sum_x_3, sum_x_2, sum_x], [sum_x_2, sum_x, line]])
    if determine != 0:
        a = toFixed(determ3([[sum_x_2_y, sum_x_y, sum_y], [sum_x_3, sum_x_2, sum_x], [sum_x_2, sum_x, line]]) / determine, 2)
        b = toFixed(determ3([[sum_x_4, sum_x_2_y, sum_x_2], [sum_x_3, sum_x_y, sum_x], [sum_x_2, sum_y, line]]) / determine, 2)
        c = toFixed(determ3([[sum_x_4, sum_x_3, sum_x_2_y], [sum_x_3, sum_x_2, sum_x_y], [sum_x_2, sum_x, sum_y]]) / determine,2)
    return a,b,c

def quad_sum_fault(x,y,lt):
    summ = 0
    for i in range(len(x)):
    	summ += pow((lt[0] * x[i] * x[i] + lt[1] * x[i] + lt[2] - y[i]), 2)
    return summ

def toFixed(num, dig):
    return float(f"{num:.{dig}f}")

def close(ex, window_linear):
    window_linear.destroy()
    root.deiconify()
    root.focus_force()
    
def close_main(event):
    root.destroy()
    root.quit()
    
def directory(event):
    root.withdraw()
    name = tk.filedialog.askopenfilename(title = 'Выберите файл', filetypes = (('TXT files', '*.txt'), ('all files', '*.*')))
    with open(name, encoding = 'utf-8') as f:
        lt = f.read().split('\n')
    use('TkAgg')
    window = tk.Tk()
    window.geometry('1350x970')
    window.configure(background = 'white')
    window.overrideredirect(1)
    window.wm_geometry("+%d+%d" % (-100, -110))
    fig = plt.figure(1, figsize = (10,10), dpi = 105)
    canvas = FigureCanvasTkAgg(fig, master = window)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row = 0, column = 0)
    plt.rc('legend', fontsize = 7)
    plt.clf()
    n = int(lt[0])
    x = [float(i[1:i.find(';')]) for i in lt[1].split(' ')]
    y = [float(i[i.find(';') + 1:-1]) for i in lt[1].split(' ')]
    y_linear = []
    y_quad = []
    x_new = []
    y_new = []
    a = linear_build_a(x, y, n)
    b = linear_build_b(x, y, n, a)
    lab_linear = tk.Label(window,text = 'Суммарная погрешность линейной апроксимирующей функции \nпри коэффициентах a = {0} и b = {1}\nравна {2}'.format(toFixed(a,2),toFixed(b,2),toFixed(linear_sum_fault(x,y,a,b),2)), font = 'Calibri 10', fg = 'black', bg = 'white')
    lab_linear.place(x = 970, y = 200)
    for i in range(len(x)):
        y_linear.append(toFixed(a * x[i] + b, 2))
    plt.plot(x,y_linear, label = 'Апроксимирующая линейная функция\n')
    sc = plt.scatter(x,y, label = 'Исходные координаты', s = 10)
    leg = plt.legend(loc = 'upper left', borderpad = 1)
    sc.set_color('black')
    leg.get_frame().set_facecolor('none')
    leg.get_frame().set_linewidth(0.0)
    x_tmp = []
    y_tmp = []
    for i in range(len(x)):
        x_tmp.append(x[i])
        y_tmp.append(y[i])
    a = toFixed(pow_build_a(x_tmp,y_tmp,n), 2)
    for i in range(len(x)):
        x_tmp[i] = x[i]
        y_tmp[i] = y[i]
    peta = toFixed(pow_build_peta(x_tmp, y_tmp, n, a), 2)
    y_pow = []
    for i in range(len(x)):
        y_pow.append(toFixed(peta * pow(x[i], a), 2))
    plt.plot(x,y_pow, label = 'Апроксимирующая степенная функция\n')
    lab_pow = tk.Label(window,text = 'Суммарная погрешность степенной апроксимирующей функции \nпри коэффициентах a = {0} и peta = {1} равна {2}'.format(toFixed(a,2),toFixed(peta,2),toFixed(pow_sum_fault(x,y,a,peta),2)), font = 'Calibri 10', fg = 'black', bg = 'white')
    lab_pow.place(x = 970, y = 350)
    leg = plt.legend(loc = 'upper left', borderpad = 1)
    leg.get_frame().set_facecolor('none')
    leg.get_frame().set_linewidth(0.0)
    for i in range(len(x)):
        x_tmp[i] = x[i]
        y_tmp[i] = y[i]
    a = toFixed(exp_build_a(x_tmp, y_tmp, n),2)
    for i in range(len(x)):
        x_tmp[i] = x[i]
        y_tmp[i] = y[i]
    peta = toFixed(exp_build_peta(x_tmp, y_tmp, n, a), 2)
    lab_exp = tk.Label(window,text = 'Суммарная погрешность экспоненциальной \nапроксимирующей функции \nпри коэффициентах a = {0} и peta = {1} равна {2}'.format(toFixed(a,2),toFixed(peta,2),toFixed(exp_sum_fault(x,y,a,peta),2)), font = 'Calibri 10', fg = 'black', bg = 'white')
    lab_exp.place(x = 970, y = 550)
    y_exp = []
    for i in range(len(x)):
        y_exp.append(toFixed(peta * exp(a * x[i]), 2))
    plt.plot(x,y_exp, label = 'Апроксимирующая экспоненциальная функция\n')
    leg = plt.legend(loc = 'upper left', borderpad = 1)
    leg.get_frame().set_facecolor('none')
    leg.get_frame().set_linewidth(0.0)
    l = quad_func(x, y)
    for i in range(len(x)):
        y_quad.append(toFixed(l[0], 2) * x[i] * x[i] + toFixed(l[1], 2) * x[i] + toFixed(l[2], 2))
    plt.plot(x,y_quad, label = 'Апроксимирующая квадратичная функция\n')
    lab_quad = tk.Label(window,text = 'Суммарная погрешность квадратичной апроксимирующей \nфункции при коэффициентах a = {0}, b = {1}\n и c = {2} равна {3}'.format(toFixed(l[0],2), toFixed(l[1],2), toFixed(l[2], 2), toFixed(quad_sum_fault(x,y,l),2)), font = 'Calibri 10', fg = 'black', bg = 'white')
    lab_quad.place(x = 970, y = 750)
    leg = plt.legend(loc = 'upper left', borderpad = 1)
    leg.get_frame().set_facecolor('none')
    leg.get_frame().set_linewidth(0.0)
    fig.canvas.draw()
    window.bind('<Escape>',  lambda ex: close(ex, window))
    
root = tk.Tk()
root.geometry('170x110')
root.configure(background = 'peru')
root.overrideredirect(1)
x = (root.winfo_screenwidth() - 200) / 2
y = (root.winfo_screenheight() - 150) / 2
lab = tk.Label(text = 'Выберите действие:', font = ('Calibri', 10, 'bold'), bg = 'peru')
lab.place(x = 20, y = 10)
root.wm_geometry("+%d+%d" % (x, y))
choice_var = tk.IntVar()
choice_var.set(0)
r1 = tk.Radiobutton(text = 'Выбрать файл', variable = choice_var, value = -1, bg = 'peru')
r1.place(x = 20, y = 40)
r1.bind('<Button-1>', directory)
root.bind('<Escape>', close_main)
root.mainloop()