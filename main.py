# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from Complex import Complex
import json


def setup():
    for i, line in enumerate(lines):
        line.set_data([], [])
        ax.add_patch(line)
    for i, circle in enumerate(circles):
        circle.center = (0, 0)
        circle.radius = 5
        ax.add_patch(circle)

        # circles[i] = plt.Circle((0, 0), 5, fill=False, ec='y')
        # ax.add_patch(lines[i])
        # ax.add_patch(circles[i])
        # setup screen and list of lines and circles.
    return patches


def dft(x):
    result = []
    N = len(x)
    for k in range(N):
        # calculate terms of dft
        term = Complex(0, 0)
        for n in range(N):
            phi = (k * n * 2 * np.pi) / N
            c = Complex(np.cos(phi), -np.sin(phi))
            term.plus(x[n].times(c))
        term.re = term.re / N
        term.im = term.im / N
        freq = k
        amp = math.sqrt((term.re * term.re + term.im * term.im))
        phase = math.atan2(term.im, term.re)
        result.append({'real': term.re,
                       'complex': term.im,
                       'frequency': freq,
                       'amplitude': amp,
                       'phase': phase})
    return result


def draw(time):
    # TODO: reset it update in the animation function.
    x = 0
    y = 0
    phi = 0
    i = 0
    for term in fourier:
        prev_x = x
        prev_y = y
        f = term['frequency']
        p = term['phase']
        r = 0.25 * term['amplitude']
        x += r * np.cos(f * time + p + phi)
        y += r * np.sin(f * time + p + phi)
        # TODO add circles and line.f
        # set circle where previous value is.
        # app.ellipse(prev_x, prev_y, r * 2, r * 2)
        lines[i].set_data([prev_x, x], [prev_y, y])
        # circles.append(plt.Circle((prev_x, prev_y), r, fill=False, ec='y'))
        circles[i].center = (prev_x, prev_y)
        circles[i].set_radius(r)
        i += 1
    return patches


def main():
    global fourier
    global ax
    global lines
    global circles
    global patches
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
    signal = []
    with open('drawing.txt') as json_file:
        data = json.load(json_file)
    for i in range(0, len(data['drawing']), 7):
        signal.append(Complex(data['drawing'][i]['x'], data['drawing'][i]['y']))
    fourier = dft(signal)
    fourier = sorted(fourier, key=lambda el: el['amplitude'], reverse=True)
    N = len(fourier)
    print("length of Fourier Transform:" + str(N))
    lines = [plt.plot([], [], 'y', linewidth=2, alpha=0.3)[0] for _ in range(N)]
    circles = [plt.Circle((0, 0 + i), 0, color='y', alpha=0.3, fill=False) for i in range(N)]
    patches = lines + circles
    plt.style.use('dark_background')
    ax.set_facecolor('black')
    print('background loaded')
    anim = animation.FuncAnimation(fig, draw,
                                   init_func=setup,
                                   frames=np.linspace(0, 2 * np.pi, N),
                                   interval=5,
                                   blit=True,
                                   repeat=False)
    print('generating gif')
    writer = animation.PillowWriter(fps=30)
    anim.save('lines_circles.gif', writer=writer)
    print('completed gif')
    plt.show()


main()
