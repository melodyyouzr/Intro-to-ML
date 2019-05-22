#!/usr/bin/env python
# coding: utf-8


import sys
import numpy as np

if __name__ == '__main__':
    train = sys.argv[1]
    word_index = sys.argv[2]
    tag_index = sys.argv[3]
    hmmprior = sys.argv[4]
    hmmemit= sys.argv[5]
    hmmtrans = sys.argv[6]

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



    f_input = open(train, 'r')
    input = f_input.readlines()
    # for i in range(10):
    #     input.append(f_input.readline())

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



    # In[174]:


    # find pi initial
    pi_count = np.zeros((len(tag_dict), 1))
    #pi = np.zeros((len(tag_dict), 1), dtype=float)
    write_pi = ""
    for m in range(len(splitdata)):
        pi_count[splitdata[m][0][1] - 1, 0] += 1
    pi_count += 1
    #print(pi_count)
    for i in range(len(tag_dict)):
        # pi[i][0] = '%.18e' %(pi_count[i][0] / np.sum(pi_count))
        # print(pi[i][0])
        write_pi = write_pi + str('%.18e' %(pi_count[i][0] / np.sum(pi_count))) + '\n'





    # Matrix A transition
    A_count = np.zeros((len(tag_dict), len(tag_dict)))
    #A = np.zeros((len(tag_dict), len(tag_dict)))
    write_A = ""

    for i in range(len(splitdata)):
        for j in range(len(splitdata[i]) - 1):
            A_count[splitdata[i][j][1] - 1, splitdata[i][j + 1][1] - 1] += 1

    A_count = A_count + 1
    # print(A_count)

    for i in range(len(tag_dict)):
        for j in range(len(tag_dict)):
            #A[i][j] = '%.18e'%A_count[i][j] / np.sum(A_count[i]))
            write_A = write_A + str('%.18e'%(A_count[i][j] / np.sum(A_count[i])))+ ' '
        write_A = write_A + '\n'




    # In[176]:


    # Matrix B emission
    B_count = np.zeros((len(tag_dict), len(word_dict)))
    #B = np.zeros((len(tag_dict), len(word_dict)))
    write_B = ""

    for i in range(len(splitdata)):
        for j in range(len(splitdata[i])):
            B_count[splitdata[i][j][1] - 1, splitdata[i][j][0] - 1] += 1


    B_count = B_count + 1
    # print(B_count)

    for i in range(len(tag_dict)):
        for j in range(len(word_dict)):
            #B[i][j] = '%.18e'%(B_count[i][j] / np.sum(B_count[i]))
            write_B = write_B + str('%.18e'%(B_count[i][j] / np.sum(B_count[i]))) + ' '
        write_B = write_B + '\n'


    prior = open(hmmprior, 'w')
    prior.write(write_pi)

    emit = open(hmmemit, 'w')
    emit.write(write_B)

    trans = open(hmmtrans, 'w')
    trans.write(write_A)

