#!/usr/bin/env python
# coding: utf-8

import csv
import sys
import numpy as np


train = sys.argv[1]
test = sys.argv[2]
train_out = sys.argv[3]
test_out = sys.argv[4]
metrics = sys.argv[5]
epoch_num = sys.argv[6]
hiddenUnits = sys.argv[7]
model_num = sys.argv[8]
lr = sys.argv[9]


def model(a, units, lr):
    if a == 1:
        alpha = np.random.uniform(-0.1, 0.1, (units, 129))
        for i in range(units):
            alpha[i][0] = 0
        beta = np.random.uniform(-0.1, 0.1, (10, units + 1))
        for i in range(10):
            beta[i][0] = 0
    else:
        alpha = np.zeros((units, 129))
        beta = np.zeros((10, units + 1))

    learningRate = lr

    return alpha, beta, learningRate



# read file
def readData(file):
    with open(file, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        rawdata = [row for row in reader]

    output = []
    for i in range(len(rawdata)):
        output.append(int(rawdata[i][0]))

    data = [[] for i in range(len(rawdata))]
    for i in range(len(rawdata)):
        data[i].append(1)
        for j in range(1, len(rawdata[0])):
            data[i].append(int(rawdata[i][j]))

    input = np.array(data)

    return input, output


# Forward
def linearFW1(x, alpha):
    a = np.matmul(alpha, x.T)
    return a


def sigmoidFW(a):
    z = []
    for i in range(len(a)):
        z.append(1 / (1 + np.exp(-a[i])))
    z.insert(0, 1)
    z = np.array(z)
    return z


def linearFW2(z, beta):
    b = np.matmul(beta, z.T)
    return b



def softmaxFW(b):
    y1 = []
    e = np.exp(b)
    for i in range(len(e)):
        y1.append(e[i] / np.sum(e))
    y1 = np.array(y1)
    return y1



# Backward
def softmaxBW(y, y1):
    gb = []
    for i in range(len(y)):
        gb.append(y1[i] - y[i])
    gb = np.array(gb)
    return gb


def linearBW1(z, gb, beta):
    beta1 = np.delete(beta, 0, 1)
    gbeta = np.matmul(gb, z.reshape(1, len(z)))
    gz = np.matmul(beta1.T, gb)
    return gbeta, gz



def sigmoidBW(z, gz):
    z = z[1:]
    z = z.reshape((len(z), 1))
    ga = gz * z * (1 - z)
    return ga


def linearBW2(x, ga):
    galpha = np.matmul(ga, x.reshape((1, len(x))))
    return galpha



def update(alpha, beta, galpha, gbeta, lr):
    alpha = alpha - lr * galpha
    beta = beta - lr * gbeta
    return alpha, beta


def epoch(a, alpha, beta, learningRate):
    # number of epoch is a.
    epoch_count = 0
    #metricsWrite = ""
    trainWrite = ""
    testWrite = ""
    for k in range(a):
        epoch_count += 1
        for i in range(len(trainIn)):
            x = trainIn[i]
            y = np.zeros((10, 1))
            y[trainOut[i]] = 1
            a = linearFW1(x, alpha)
            z = sigmoidFW(a)
            b = linearFW2(z, beta)
            y1 = softmaxFW(b)
            gb = softmaxBW(y, y1)
            gbeta, gz = linearBW1(z, gb, beta)
            ga = sigmoidBW(z, gz)
            galpha = linearBW2(x, ga)
            alpha, beta = update(alpha, beta, galpha, gbeta, learningRate)

        # train entropy
        traincrossEntropy = 0
        for i in range(len(trainIn)):
            x = trainIn[i]
            y = np.zeros((10, 1))
            y[trainOut[i]] = 1
            a = linearFW1(x, alpha)
            z = sigmoidFW(a)
            b = linearFW2(z, beta)
            y1 = softmaxFW(b)
            for j in range(10):
                traincrossEntropy += y[j] * np.log(y1[j])

        traincrossEntropy = -1 / len(trainIn) * traincrossEntropy
        trainWrite = trainWrite + str(traincrossEntropy[0]) + '\n'
        #metricsWrite = metricsWrite + "epoch=" + str(epoch_count) + " crossentropy(train): " + str(traincrossEntropy[0]) + '\n'
        print("train:")
        print(traincrossEntropy[0])

        # test entropy
        testcrossEntropy = 0
        for i in range(len(testIn)):
            x = testIn[i]
            y = np.zeros((10, 1))
            y[testOut[i]] = 1
            a = linearFW1(x, alpha)
            z = sigmoidFW(a)
            b = linearFW2(z, beta)
            y1 = softmaxFW(b)
            for j in range(10):
                testcrossEntropy += y[j] * np.log(y1[j])

        testcrossEntropy = -1 / len(testIn) * testcrossEntropy
        testWrite = testWrite + str(testcrossEntropy[0]) + '\n'
        #metricsWrite = metricsWrite + "epoch=" + str(epoch_count) + " crossentropy(test): " + str(testcrossEntropy[0]) + '\n'
        print("test:")
        print(testcrossEntropy[0])


    # # train error
    # index = ""
    # trainError = 0
    # for i in range(len(trainIn)):
    #     x = trainIn[i]
    #     y = np.zeros((10, 1))
    #     y[trainOut[i]] = 1
    #     a = linearFW1(x, alpha)
    #     z = sigmoidFW(a)
    #     b = linearFW2(z, beta)
    #     y1 = softmaxFW(b)
    #     m = np.argmax(y1, axis=0)
    #     index = index + str(m) + '\n'
    #     if (m != trainOut[i]):
    #         trainError += 1
    # trainErrorRate = trainError / len(trainOut)
    # metricsWrite = metricsWrite + 'error(train): ' + str(trainErrorRate) + '\n'
    # print(trainErrorRate)
    #
    # # test error
    # testindex = ""
    # testError = 0
    # for i in range(len(testIn)):
    #     x = testIn[i]
    #     y = np.zeros((10, 1))
    #     y[testOut[i]] = 1
    #     a = linearFW1(x, alpha)
    #     z = sigmoidFW(a)
    #     b = linearFW2(z, beta)
    #     y1 = softmaxFW(b)
    #     n = np.argmax(y1, axis=0)
    #     testindex = testindex + str(n) + '\n'
    #     if (n != testOut[i]):
    #         testError += 1
    # testErrorRate = testError / len(testOut)
    # metricsWrite = metricsWrite + 'error(test): ' + str(testErrorRate) + '\n'
    # print(testErrorRate)

    return trainWrite, testWrite
    #return trainWrite, testWrite


trainIn, trainOut = readData(train)
testIn, testOut = readData(test)
a, b, lr_ = model(int(model_num), int(hiddenUnits), float(lr))
k, l = epoch(int(epoch_num), a, b, lr_)

# metrics_file = open(metrics, 'w')
# metrics_file.write(g)

trainOut_file = open(train_out, 'w')
trainOut_file.write(k)

testOut_file = open(test_out, 'w')
testOut_file.write(l)


