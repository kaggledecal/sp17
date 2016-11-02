import numpy as np
import activation_function as act
'''
Collection of common neural network cost functions.
API based on the implementation in
http://neuralnetworksanddeeplearning.com/chap2.html
Specifically:
https://github.com/mnielsen/neural-networks-and-deep-learning/blob/master/src/network2.py

TODO: Add something that actually uses gprime and calculates deriv
'''
class CrossEntropy:
    ''' cross entropy and softmax regression '''
    @staticmethod
    def fn(yhat, y):
        return - np.sum(y * np.log(yhat + 1e-100))
    @staticmethod
    def delta(z, yhat, y, gprime=act.Softmax.deriv):
        return yhat - y
class Quadratic:
    '''Mean Squared Errors Implementation'''
    @staticmethod
    def fn(yhat, y):
        return np.norm(y - yhat)**2 /2
    def delta(z, yhat, y, gprime):
        return yhat - y
