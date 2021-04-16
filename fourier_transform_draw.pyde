from collections import deque
from Complex import Complex
from Imaging import ImageCleaning
import json


time=0
path = deque()
signal = []
fourier = deque()


def setup():
    global scan
    scan = ImageCleaning('fourier_image.jpg')
    scan.contourscaling() 
    with open('drawing.txt') as json_file:
        data = json.load(json_file)
    global fourier    
    for i in range(0,len(data['drawing']),5):
        signal.append(Complex(data['drawing'][i]['x'], data['drawing'][i]['y']))
    fourier = dft(signal)
    fourier = sorted(fourier, key=lambda el: el['amplitude'],reverse=True)
    size(800, 800) 

def dft(x):
    result = [] 
    N = len(x)
    for k in range(N):
        #calculate terms of dft
        sum = Complex(0,0)        
        for n in range(N):
            phi = (k*n*2*PI)/ N
            c = Complex(cos(phi), -sin(phi))
            sum.plus(x[n].times(c))        
        sum.re = sum.re / N
        sum.im = sum.im / N        
        freq = k
        amp = sqrt(sum.re*sum.re + sum.im*sum.im)
        phase = atan2(sum.im, sum.re)                
        result.append({'real':sum.re,
                       'complex': sum.im,
                       'frequency': freq,
                       'amplitude': amp,
                       'phase': phase})         
    return result
    
def epiCycles(x,y,phi,series):
    for term in series:
        prevx = x
        prevy = y        
        f = term['frequency']
        p = term['phase']
        r = 1*term['amplitude']
        x += r * cos(f * time + p + phi)
        y += r * sin(f * time + p + phi)        
        ellipse(prevx,prevy, r*2,r*2)        
        line(prevx,prevy,x,y)
        pushMatrix();    
        translate(x, y);
        rotate(atan2(y-prevy, x-prevx));
        fill(255,50)
        stroke(255,50)
        triangle(0, 0, -5, 1.5,   -5, -1.5);
        noFill()
        popMatrix();     
    return PVector(x,y)

    
def draw():
    global time
    global wave
    background(0)
       
    image(scan.img, 0,0, width, height)
    stroke(255,100)
    v = epiCycles(width/2,height/2, 0, fourier)
    path.appendleft(v)
    stroke(255)   
    beginShape();    
    noFill();
    for i in range(len(path)):
        vertex(path[i].x, path[i].y)  
    endShape();    
    if time >= TWO_PI:
        path.pop()
    dt = TWO_PI / len(fourier)
    time += dt
