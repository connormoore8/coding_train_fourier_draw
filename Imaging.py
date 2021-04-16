class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)
        
        
        
    def brightscaling(self, thresh):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        result.loadPixels()
        for x in xrange(self.img.width):
            for y in xrange(self.img.height):
                index = x + y*self.img.width
                # print(brightness(self.img.pixels[index]))
                if (brightness(self.img.pixels[index]) > thresh):
                    result.pixels[index]  = color(255) # White
                else:
                    result.pixels[index]  = color(0)   # Black
        result.updatePixels()
        self.img = result
        
        # self.img = image(result.updatePixels(),0,0)
