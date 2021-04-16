sobelX = [[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]]
sobelY= [[-1, -2, -1], [0, 0, 0],[1, 2, 1]]

class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)
        self.sX = [[-1, 0, 1] , [-2, 0, 2] , [-1, 0, 1]]
        self.sY = [[-1, -2, -1] , [0, 0, 0] , [1, 2, 1]]
        
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
                result.pixels[index] = self.convolute(index,self.sX)
                result.pixels[index] = self.bright(index, 127)
                # result.pixels[index] = sqrt(self.convolute(index,self.sX)**2 + self.convolute(index, self.sY)**2)
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
        
    
    def convolute(self, index, matrix):
        rval = 0.0
        gval = 0.0
        bval = 0.0
        for x in range(len(matrix)):
            for y in range(len(matrix)):
                loc = (x-1) + index + (y-1) * self.img.width 
                loc = constrain(loc, 0, len(self.img.pixels)-1)
                rval += (red(self.img.pixels[loc]) * matrix[x][y])
                gval += (green(self.img.pixels[loc]) * matrix[x][y])
                bval += (blue(self.img.pixels[loc]) * matrix[x][y])
        rval = constrain(rval, 0, 255)
        gval = constrain(gval, 0, 255)
        bval = constrain(bval, 0, 255)
        return color(rval, gval, bval)
