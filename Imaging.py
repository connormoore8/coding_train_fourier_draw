sobelX = [[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
sobelY= [[-1, -2, -1], [0, 0, 0],[1, 2, 1]]
flat = [[1,1,1,1,1] for x in range(5)] 
class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)
        self.sX = [[-1, 0, 1] , [-2, 0, 2] , [-1, 0, 1]]
        self.sY = [[-1, -2, -1] , [0, 0, 0] , [1, 2, 1]]
        self.flat = flat
        
    def brightscaling(self,thresh):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                # print(brightness(self.img.pixels[index]))
                result.pixels[index] = self.bright(index,thresh)
        result.updatePixels()
        self.img = result
        
    def contourscaling(self):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                result.pixels[index] = self.contour_differential(index)
        result.updatePixels()
        self.img = result
        
        
    def sobelscaling(self):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                result.pixels[index] = self.convolute_Sobel(index)                
        result.updatePixels()
        self.img = result
        
        
    def flatscaling(self):
        print(self.flat)
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                result.pixels[index] = self.convolute_Flatten(index)                
        result.updatePixels()
        self.img = result
        
        
        
    def contour_differential(self, index1):
        return abs(brightness(self.img.pixels[index1-1]) - brightness(self.img.pixels[index1]))*1.1
              
        
    def bright(self, index, thresh):
        # print(brightness(self.img.pixels[index]))
        if (brightness(self.img.pixels[index]) > thresh):
            return color(0) # Black
        else:
            return color(255)# White
        
    
    def convolute_Sobel(self, index):
        rval = 0.0
        gval = 0.0
        bval = 0.0
        for x in range(len(self.sX)):
            for y in range(len(self.sX)):
                loc = (x-1) + index + (y-1) * self.img.width 
                loc = constrain(loc, 0, len(self.img.pixels)-1)
                rval += sqrt(sq(red(self.img.pixels[loc]) * self.sX[x][y])
                             +sq(red(self.img.pixels[loc]) * self.sY[x][y]))
                gval += sqrt(sq(green(self.img.pixels[loc]) * self.sX[x][y])
                             +sq(green(self.img.pixels[loc]) * self.sY[x][y]))
                bval += sqrt(sq(blue(self.img.pixels[loc]) * self.sX[x][y])
                             +sq(blue(self.img.pixels[loc]) * self.sY[x][y]))
        rval = constrain(rval, 0, 255)
        gval = constrain(gval, 0, 255)
        bval = constrain(bval, 0, 255)
        return color(rval, gval, bval)
    
    
    
    def convolute_Flatten(self, index):
        rval = 0.0
        gval = 0.0
        bval = 0.0
        for x in range(len(self.flat)):
            for y in range(len(self.flat)):
                loc = (x-1) + index + (y-1) * self.img.width 
                loc = constrain(loc, 0, len(self.img.pixels)-1)
                rval += (red(self.img.pixels[loc]) * self.flat[x][y])
                gval += (green(self.img.pixels[loc]) * self.flat[x][y])
                bval += (blue(self.img.pixels[loc]) * self.flat[x][y])
        rval = constrain(rval, 0, 255)
        gval = constrain(gval, 0, 255)
        bval = constrain(bval, 0, 255)
        return color(rval/25, gval/25, bval/25)
    
