class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)

        
    def brightscaling(self,thresh):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                # print(brightness(self.img.pixels[index]))
                result.pixels[index] = self.bright(self, index)
        result.updatePixels()
        self.img = result
        
    def contourscaling(self):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                leftIndex = (x-1) + y*self.img.width
                result.pixels[index] = self.contour_differential(leftIndex, index)
        result.updatePixels()
        self.img = result
        
    def contour_differential(self, Index1, Index2):
        return abs(brightness(self.img.pixels[Index1]) - brightness(self.img.pixels[Index2]))
              
        
    def bright(self, index):
        # print(brightness(self.img.pixels[index]))
        if (brightness(self.img.pixels[index]) > 127):
            return color(0) # Black
        else:
            return color(255)   # White
        
    
    
