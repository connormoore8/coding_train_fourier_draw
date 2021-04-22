# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import math
from Complex import Complex
# from Imaging import ImageCleaning
import json

# def setup():
#     path = deque()
#
#     # circles = [plt.Circle((0,0), 15, fill=False, ec='y')[0] for x in range(len(fourier))]
#     #setup screen and list of lines and circles.
#     return tuple(lines)

def dft(x):
    result = []
    N = len(x)
    for k in range(N):
        # calculate terms of dft
        sum = Complex(0, 0)
        for n in range(N):
            phi = (k * n * 2 * np.pi) / N
            c = Complex(np.cos(phi), -np.sin(phi))
            sum.plus(x[n].times(c))
        sum.re = sum.re / N
        sum.im = sum.im / N
        freq = k
        amp = math.sqrt((sum.re * sum.re + sum.im * sum.im))
        phase = math.atan2(sum.im, sum.re)
        result.append({'real': sum.re,
                       'complex': sum.im,
                       'frequency': freq,
                       'amplitude': amp,
                       'phase': phase})
    return result


def epicycles(lines, circles, time, x, y, phi, series):
    #TODO: untangle for update function in animation.
    i = 0
    for term in series:
        prevx = x
        prevy = y
        f = term['frequency']
        p = term['phase']
        r = 1 * term['amplitude']
        x += r * np.cos(f * time + p + phi)
        y += r * np.sin(f * time + p + phi)
        #TODO add circles and line.f
        # set circle where previouse value is.
        # app.ellipse(prevx, prevy, r * 2, r * 2)
        lines[i].set_data([prevx, x],[prevy, y])
        # set line between two spots.
        # app.line(prevx, prevy, x, y)
        i += 1
        # if i > 3: return {'x': x, 'y': y}
    return {'x': x, 'y': y}


def draw(time):
    #TODO: reset it update in the animation function.
    # global wave
    # app.image(scan.img, 0, 0, app.width, app.height)
    #print(fourier)
    # epicycles(lines, circles, time, 0, 0, 0, fourier)
    x = 0
    y = 0
    phi = 0
    i = 0
    for term in fourier:
        # print(lines[0])
        prevx = x
        prevy = y
        f = term['frequency']
        p = term['phase']
        r = 0.15 * term['amplitude']
        x += r * np.cos(f * time + p + phi)
        y += r * np.sin(f * time + p + phi)
        # TODO add circles and line.f
        # set circle where previouse value is.
        # app.ellipse(prevx, prevy, r * 2, r * 2)
        lines[i].set_data([prevx, x], [prevy, y])
        # print(lines[i])
    # path.appendleft(v)
    # app.stroke(255)
    # app.beginShape()
    # app.noFill()


    # for i in range(len(path)):
    #     vertex(path[i].x, path[i].y)
    # endShape();
    # if time >= TWO_PI:
    #     path.pop()
    # dt = TWO_PI / len(fourier)
    # time += dt
    return lines

def main():
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
    signal = []
    with open('drawing.txt') as json_file:
        data = json.load(json_file)
    global fourier
    global lines
    global circles
    for i in range(0, len(data['drawing']), 5):
        signal.append(Complex(data['drawing'][i]['x'], data['drawing'][i]['y']))
    fourier = dft(signal)
    fourier = sorted(fourier, key=lambda el: el['amplitude'], reverse=True)
    lines = [ax.plot([], [], color='black', linewidth=2)[0] for x in range(len(fourier))]
    print('lines created')
    plt.style.use('dark_background')
    print('background loaded')
    anim = animation.FuncAnimation(fig, draw,
                                   frames=np.linspace(0,2*np.pi, len(fourier)),
                                   interval=40,
                                   blit=True)

    plt.show()


main()
