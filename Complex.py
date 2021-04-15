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
