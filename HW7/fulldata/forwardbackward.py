 #!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import numpy as np


def logsumexp(x, y):
    if x == float("-inf"):
        return y
    if y == float("-inf"):
        return x
    m = max(x, y)
    sum = m + np.log(1 + np.exp(-abs(x - y)))
    return sum


# In[8]:


def alpha_beta(data, tag_dict, a, b):
    # alpha of first sentence
    alpha = np.zeros((len(data), len(tag_dict)))
    xt = data[0][0]
    # first row of alpha
    alpha_n = np.add(b[:, xt - 1], pi)
    alpha[0] = alpha_n

    # start from the second word
    for i in range(1, len(data)):
        xi = data[i][0] - 1
        for j in range(len(tag_dict)):
            sum = float("-inf")
            new_matrix = a[:, j] + alpha[i - 1]
            for n in new_matrix:
                sum = logsumexp(sum, n)

            alpha[i][j] = sum + b[j][xi]

    beta = np.zeros((len(data), len(tag_dict)))

    for i in range(len(data) - 1, 0, -1):
        xi = data[i][0] - 1
        for j in range(len(tag_dict)):
            sum = float("-inf")
            new_matrix = b[:, xi] + beta[i] + a[j]
            for n in new_matrix:
                sum = logsumexp(sum, n)
            beta[i - 1][j] = sum

    return alpha, beta


# In[14]:


# predict
def predict(alpha, beta, data, word_dict):
    predict_matrix = alpha + beta
    y_pre = np.argmax(predict_matrix, axis=1) + 1
    y_pre_tag = []
    for index in y_pre:
        for k, v in tag_dict.items():
            if (v == index):
                y_pre_tag.append(k)

    word = []
    for i in range(len(data)):
        for k, v in word_dict.items():
            if (v == data[i][0]):
                word.append(k)

    output = ""
    for i in range(len(word)):
        output = output + word[i] + '_' + y_pre_tag[i]
        if i == len(word) - 1:
            output = output + '\n'
        else:
            output = output + ' '


    return output, y_pre


# In[15]:


def log_likelihood(alpha):
    last_row = alpha[len(alpha) - 1]
    likelihood = float('-inf')
    for k in last_row:
        likelihood = logsumexp(likelihood, k)
    print(likelihood)
    return likelihood


if __name__ == '__main__':
    test = sys.argv[1]
    word_index = sys.argv[2]
    tag_index = sys.argv[3]
    hmmprior = sys.argv[4]
    hmmemit = sys.argv[5]
    hmmtrans = sys.argv[6]
    prediction = sys.argv[7]
    metric = sys.argv[8]


    pi = np.loadtxt(hmmprior)
    pi = np.log(pi)


    a = np.loadtxt(hmmtrans)
    a = np.log(a)


    b = np.loadtxt(hmmemit)
    b = np.log(b)


    f_tag = open(tag_index, 'r')
    tag = f_tag.readlines()
    tag_dict = {}
    for i in range(len(tag)):
        tag_dict[tag[i].strip('\n')] = i + 1


    f_word = open(word_index, 'r')
    word = f_word.readlines()
    word_dict = {}
    for i in range(len(word)):
        word_dict[word[i].strip('\n')] = i + 1


    f_input = open(test, 'r')
    input = f_input.readlines()
    traindata = []
    for i in range(len(input)):
        sentence = input[i].strip('\n')
        word = sentence.split(' ')
        traindata.append(word)

    splitdata = []
    for i in range(len(traindata)):
        sentence_line = []
        for j in range(len(traindata[i])):
            word_line = []
            splitword = traindata[i][j].split('_')[0]
            splittag = traindata[i][j].split('_')[1]
            word_line.append(splitword)
            word_line.append(splittag)
            sentence_line.append(word_line)

        splitdata.append(sentence_line)

    for i in range(len(splitdata)):
        for j in range(len(splitdata[i])):
            splitdata[i][j][0] = word_dict.get(splitdata[i][j][0])
            splitdata[i][j][1] = tag_dict.get(splitdata[i][j][1])

    total_likelihood = 0
    count = 0
    num_word = 0
    predicttest = ""
    for data in splitdata:
        m, n = alpha_beta(data, tag_dict, a, b)
        print(m)
        print(n)
        total_likelihood += log_likelihood(m)
        out, tag_compare = predict(m, n, data, word_dict)
        predicttest += out
        num_word += len(data)
        for i in range(len(data)):
            if data[i][1] == tag_compare[i]:
                count += 1

    accuracy = count / num_word
    ave_likelihood = total_likelihood / len(splitdata)

    predict_file = open(prediction, 'w')
    predict_file.write(predicttest)

    metric_file = open(metric, 'w')
    metric_file.write("Average Log-Likelihood: %.8f\n" %ave_likelihood)
    metric_file.write("Accurary: %.12f\n" %accuracy)







