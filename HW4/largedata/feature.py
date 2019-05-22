#!/usr/bin/env python
# coding: utf-8

# In[55]:


import sys
import csv

# In[57]:


def model1(inputfile, outputfile):    
    with open(inputfile) as csvfile :
        reader = csv.reader(csvfile, delimiter ="\t")
        rawdata = [row for row in reader]

    splitdata = [[] for i in range(len(rawdata))]
    for i in range(len(rawdata)): 
        splitdata[i] = rawdata[i][1].split()

    output = ""
    for i in range(len(splitdata)):
        newdict = {}
        output = output + rawdata[i][0] + "\t"
        for eachword in splitdata[i]:
            newdict[eachword] = dic.get(eachword)
        for v in newdict.values():
            if v != None:
                output = output + v + ":1" + "\t"
        output = output + "\n"

    outfile = open(outputfile,"w")
    outfile.write(output)
    outfile.close()


# In[59]:


def model2(inputfile, outputfile):
    with open(inputfile) as csvfile :
        reader = csv.reader(csvfile, delimiter ="\t")
        rawdata = [row for row in reader]

    splitdata = [[] for i in range(len(rawdata))]
    for i in range(len(rawdata)): 
        splitdata[i] = rawdata[i][1].split()
        
    output = ""
    for i in range(len(splitdata)):
        newdict = {}
        output = output + rawdata[i][0] + "\t"
        for word1 in splitdata[i]:
            count = 0
            for word2 in splitdata[i]:
                if word1 == word2:
                    count += 1
            if count < 4:
                newdict[word1] = dic.get(word1)

        for v in newdict.values():
            if (v != None):
                output = output + v + ":1" + "\t"
        output = output + "\n"


    model2_out = open(outputfile,"w")
    model2_out.write(output)

    model2_out.close()

# In[187]:


input_train = sys.argv[1]
input_valid = sys.argv[2]
input_test = sys.argv[3]
input_dict = sys.argv[4]
output_train = sys.argv[5]
output_valid = sys.argv[6]
output_test = sys.argv[7]
modelflag = sys.argv[8]

with open(input_dict,'r') as f:
    dic = []
    for line in f.readlines():
        line = line.strip().split(' ')
        dic.append(line)

dic = dict(dic)

if modelflag == "1":
    model1(input_train, output_train)
    model1(input_valid, output_valid)
    model1(input_test, output_test)

if modelflag == "2":
    model2(input_train, output_train)
    model2(input_valid, output_valid)
    model2(input_test, output_test)

