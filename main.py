# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
from Complex import Complex
import json
fourier = []
fig = plt.figure(figsize=(10, 10))
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
lines = []
circles = []
patches = lines + list(circles)


def setup():
    for i in range(len(fourier)):
        lines.append(ax.plot([], [], color='y', lw=2)[0])
        circles.append(plt.Circle((0, 0), 5, fill=False, ec='y'))
    # circles = [plt.Circle((0,0), 15, fill=False, ec='y')[0] for x in range(len(fourier))]
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
    # global wave
    # app.image(scan.img, 0, 0, app.width, app.height)
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
        circles[i].set_radius(r)
        circles[i].center = (prev_x, prev_y)
        i += 1
    return patches


def main():
    global fourier
    signal = []
    with open('drawing.txt') as json_file:
        data = json.load(json_file)
    for i in range(0, len(data['drawing']), 5):
        signal.append(Complex(data['drawing'][i]['x'], data['drawing'][i]['y']))
    fourier = dft(signal)
    fourier = sorted(fourier, key=lambda el: el['amplitude'], reverse=True)
    print(len(fourier))
    plt.style.use('dark_background')
    print('background loaded')
    anim = animation.FuncAnimation(fig, draw,
                                   init_func=setup,
                                   frames=np.linspace(0, 2*np.pi, len(fourier)),
                                   interval=20,
                                   blit=True,
                                   repeat=False)
    print('generating gif')
    writer = animation.PillowWriter(fps=25)
    anim.save('lines.gif', writer=writer)
    print('completed gif')
    plt.show()


main()
