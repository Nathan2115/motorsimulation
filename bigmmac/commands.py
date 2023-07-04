"""`commands.py` provides control input generation for BigMMAC. """

class Step:
    """`Step` provides a step input generation.This class is initialized with an amplitude, and simply returns that amplitude
    with the `get()` method whenever called."""
    def __init__(self, amplitude):
        self.amplitude = amplitude
    def get(self):
        return self.amplitude
        
