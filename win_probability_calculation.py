import numpy as np

class WinProbabilityCalculator:
    def __init__(self, k=0.15, M0=0):
        self.k = k
        self.M0 = M0

    def weighted_win_probability(self, momentum, inning):
        """
        Calculate the win probability based on momentum and inning."""

        inning_weight = np.log1p(inning)  
        adjusted_momentum = momentum * inning_weight
        return 1 / (1 + np.exp(-self.k * (adjusted_momentum - self.M0)))
 