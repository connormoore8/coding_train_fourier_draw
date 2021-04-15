from collections import deque
import json
time=0
path = deque()
signal = []
fourier = deque()



class Complex: 
    
    def __init__(self, real, imaginary):
        self.re = real
        self.im = imaginary
        
    def plus(self, complex_number):
        self.re += complex_number.re
        self.im += complex_number.im    
    
    def times(self, complex_number):
        return Complex(self.re*complex_number.re - self.im * complex_number.im,
                   self.re*complex_number.im + self.im*complex_number.re)


def setup():
    with open('drawing.txt') as json_file:
        data = json.load(json_file)
        
    
    # print(data['drawing'])
    global fourier    
    for i in range(0,len(data['drawing']),5):
        signal.append(Complex(data['drawing'][i]['x'], data['drawing'][i]['y']))
    # for i in range(100):
    #     angle = map(i, 0, 100, 0, TWO_PI)
    #     signal.append(Complex(50*noise(angle),50*noise(angle+1000)))
        
    fourier = dft(signal)
    fourier = sorted(fourier, key=lambda el: el['amplitude'],reverse=True)
    #print(fourier)
    # frameRate(60)
    size(1600, 1600)
   


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
    # for line in result:
    #      print(line)
    return result
    
def epiCycles(x,y,phi,series):
    for term in series:
        prevx = x
        prevy = y
        
        f = term['frequency']
        p = term['phase']
        r = 3*term['amplitude']
        # print(type(f))
        x += r * cos(f * time + p + phi)
        y += r * sin(f * time + p + phi)
        
        ellipse(prevx,prevy, r*2,r*2)
        
        line(prevx,prevy,x,y)
        
        # pushMatrix();    
        # translate(v.x, v.y);
        # rotate(PI / 2);
        # fill(255)
        # triangle(0, 0, -5, 1.5,   -5, -1.5);
        # popMatrix();
        
        
    return PVector(x,y)

    
def draw():
    global time
    global wave
    stroke(255,100)
    background(0)
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
