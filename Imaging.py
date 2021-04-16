class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)
        
        
        
    def brightscaling(self, thresh):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                # print(brightness(self.img.pixels[index]))
                if (brightness(self.img.pixels[index]) > thresh):
                    result.pixels[index]  = color(0) # White
                else:
                    result.pixels[index]  = color(255)   # Black
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
                result.pixels[index]  = abs(brightness(self.img.pixels[index]) 
                                            - brightness(self.img.pixels[leftIndex]))
        result.updatePixels()
        self.img = result
