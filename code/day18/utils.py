import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def load_mnist_dataset():
    '''
    Loads the mnist dataset from a folder
    :return: The training and tessting sets as specified by the mnist package
    '''
    mndata = pd.read_csv('../../datasets/MNIST/train.csv')
    labels_train = mndata['label']
    X_train = mndata.drop('label', axis=1).as_matrix()
    return X_train, labels_train
def one_hot(labels_train, num_classes=10):
    '''Convert categorical labels to standard basis vectors in R^{num_classes} '''
    return np.eye(num_classes)[labels_train]
def train_test_split(data, labels, test_size=1/6):
    assert len(data) == len(labels), "Data and labels are mismatched lengths"
    indices = np.random.permutation(data.shape[0])
    train_test_index = int(len(labels) * test_size)
    test_idx, training_idx = indices[:train_test_index], indices[train_test_index:]
    X_train, X_test = data[training_idx,:], data[test_idx,:]
    y_train, y_test = labels[training_idx,:], labels[test_idx,:]
    return X_train, y_train, X_test, y_test
def plot_mnist(digit, title=None):
    assert len(digit.shape) < 3, "Digit must be a vector or matrix, not bigger"
    if 784 in digit.shape:
        digit = digit.reshape((28,28))
    if title:
        plt.title(title)
    plt.imshow(digit, cmap='gray')
    plt.show()