#!/usr/bin/env python
# coding: utf-8

# In[238]:
import sys
import csv
import numpy as np


# In[239]:


def sparse_dot(x,w):
    product = 0.0
    for i,v in x.items():
        product += v*w[i]
    return product

def epoch(a):
    theta = [0] * 39177
    likelihood_list = []
    # a epoch.
    for k in range(a):
        # one epoch, update theta N times.
        for i in range(example_length):
            yi = float(rawdata[i][0])
            xi = list[i]
            dotproduct = sparse_dot(xi, theta)

            num = yi - (np.exp(dotproduct)/(1 + np.exp(dotproduct))) 
            #print(num)
            for i in xi.keys():
                theta[i] = theta[i] + 0.1 * num 

        for i in range(example_length):
            xi = list[i]
            yi = float(rawdata[i][0])     
            likelihood = -yi(sparse_dot(xi, theta)) + np.log(1+sparse_dot(xi, theta)，e)

        lilelihood_list.append(likelihood)


    return theta


# In[240]:


def predict_label(final_theta):
    # function of label predict
    label_list = ""
    label_count = 0
    for i in range(example_length):
        final_product = sparse_dot(list[i], final_theta)
        #print(final_product)
        probability = 1/(1 + np.exp(-final_product))
        #print(probability)
        if probability > 0.5:
            label = "1"
        else:
            label = "0"
        label_list = label_list + label + '\n'
        if label != rawdata[i][0]:
            label_count += 1
        
        
    error = label_count / example_length
    return error, label_list


# In[241]:


#main
format_train = sys.argv[1]
format_valid = sys.argv[2]
format_test = sys.argv[3]
input_dict = sys.argv[4]
out_train = sys.argv[5]
out_test = sys.argv[6]
metrics = sys.argv[7]
epoch_num = sys.argv[8]

# train data
with open(format_train) as csvfile :
    reader = csv.reader(csvfile, delimiter ="\t")
    rawdata = [row for row in reader]

list = []
example_length = len(rawdata)

for i in range (example_length):
    example_dict = {}
    example_dict[0] = 1
    length = len(rawdata[i][1:-1])
    for j in range(length):
        key = int(rawdata[i][j + 1].split(":")[0])
        example_dict[key] = 1
    list.append(example_dict)

theta = epoch(int(epoch_num))
error_train, train_label_list = predict_label(theta)

train_out = open(out_train,'w')
train_out.write(train_label_list)


# test data
with open(format_test) as csvfile :
    reader = csv.reader(csvfile, delimiter ="\t")
    rawdata = [row for row in reader]

list = []
example_length = len(rawdata)

for i in range (example_length):
    example_dict = {}
    example_dict[0] = 1
    length = len(rawdata[i][1:-1])
    for j in range(length):
        key = int(rawdata[i][j + 1].split(":")[0])
        example_dict[key] = 1
    list.append(example_dict)
    
error_test, test_label_list = predict_label(theta)

test_out = open(out_test,'w')
test_out.write(test_label_list)


#error
error_file = open(metrics,'w')
error_file.write('error(train): ' + str(error_train)+'\n')
error_file.write('error(test): ' + str(error_test))


# In[ ]:




