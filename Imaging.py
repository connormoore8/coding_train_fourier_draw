class ImageCleaning:
    
    def __init__(self,address):
        self.img = loadImage(address)
        
    def brightscaling(self, thresh):
        self.img.loadPixels()
        result = createImage(self.img.width, self.img.height, RGB)
        for x in range(self.img.width):
            for y in range(self.img.height):
                index = x + y*self.img.width
                if (brightness(self.img.pixels[index]) > thresh):
                    result.pixels[index]  = color(255) # White
                else:
                    result.pixels[index]  = color(0)   # Black
        self.img = image(result.updatePixels(),0,0)
