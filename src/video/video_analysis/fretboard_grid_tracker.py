import numpy as np

class FretboardGridTracker:
    def __init__(self, alpha=0.7):
        self.alpha = alpha  # suavização temporal
        self.frets = None
        self.strings = None

    def initialize(self, frets, strings):
        self.frets = np.array(frets, dtype=float)
        self.strings = np.array(strings, dtype=float)

    def update(self, frets, strings):
        frets = np.array(frets, dtype=float)
        strings = np.array(strings, dtype=float)

        if self.frets is None or self.strings is None:
            self.initialize(frets, strings)
            return self.frets, self.strings

        # Garantir correspondência por índice
        if len(frets) == len(self.frets):
            self.frets = (
                self.alpha * self.frets +
                (1 - self.alpha) * frets
            )

        if len(strings) == len(self.strings):
            self.strings = (
                self.alpha * self.strings +
                (1 - self.alpha) * strings
            )

        return self.frets, self.strings
