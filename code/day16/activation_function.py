import numpy as np
import scipy as sp
def safe_exp(x):
    '''to avoid inf and NaN values'''
    return np.exp(sp.clip(x, -500, 500))

class Sigmoid:
    @staticmethod
    def fn(x):
        return 1.0/(1.0+safe_exp(   -x))
    @staticmethod
    def deriv(x):
        sig = Sigmoid.fn(x)
        return sig * (1 - sig)
class Softmax:
    @staticmethod
    def fn(x):
        return safe_exp(x) / np.sum(safe_exp(x), axis=0)
    @staticmethod
    def deriv(x):
        ''' lol'''
        return 0
class ReLU:
    @staticmethod
    def fn(x):
        return np.maximum(x, 0)
    @staticmethod
    def deriv(x):
        return np.where(x > 0, 1, 0)

