import sys
import csv
import copy
from math import log

class Node:
    data = []

    def __init__(self, data, l, r, attr):
        self.data = data
        self.left = l
        self.right = r
        self.attrvalue = attr

def loadData(data):

    # save the data column by column
    numberlist = [[] for i in range(len(data[0]))]
    for i in range(0, len(data[0])):
        for j in range(0, len(data)):
            numberlist[i].append(data[j][i])

    return numberlist

def muturalinformation(numberlist):

    # H(xi) & H(y)
    h = []
    length = float(len(numberlist[0]))

    for i in range(0, len(numberlist)):
        count = 0
        for j in numberlist[i]:
            count = count + int(j)

        if count != 0:
            entropy1 = -(count / length) * log(count / length, 2)
        else:
            entropy1 = 0

        if length - count != 0:
            entropy2 = -((length - count) / length) * log((length - count) / length, 2)
        else:
            entropy2 = 0

        entropy = entropy1 + entropy2
        h.append(entropy)


    # H(xi,y)
    h1 = []
    for i in range(len(numberlist) - 1):
        num = 0
        num1 = 0
        num2 = 0
        num3 = 0
        for j in range(len(numberlist[0])):
            if (numberlist[i][j] == numberlist[i][0]) and (numberlist[-1][j] == numberlist[-1][0]):
                num += 1
            elif (numberlist[i][j] == numberlist[i][0]) and (numberlist[-1][j] != numberlist[-1][0]):
                num1 += 1
            elif (numberlist[i][j] != numberlist[i][0]) and (numberlist[-1][j] == numberlist[-1][0]):
                num2 += 1
            elif (numberlist[i][j] != numberlist[i][0]) and (numberlist[-1][j] != numberlist[-1][0]):
                num3 += 1
        if num != 0:
            entropy1 = -(num / length) * log(num / length, 2)
        else:
            entropy1 = 0
        if num1 != 0:
            entropy2 = -(num1 / length) * log(num1 / length, 2)
        else:
            entropy2 = 0
        if num2 != 0:
            entropy3 = -(num2 / length) * log(num2 / length, 2)
        else:
            entropy3 = 0
        if num3 != 0:
            entropy4 = -(num3 / length) * log(num3 / length, 2)
        else:
            entropy4 = 0
        entropy = entropy1 + entropy2 + entropy3 + entropy4
        h1.append(entropy)

    # MI =  H(xi) + H(y) - H(xi,y)
    mi = []
    for i in range(len(numberlist) - 1):
        a = h[i] + h[-1] - h1[i]
        mi.append(a)

    # Which attribute to choose
    maxvalue = max(mi)
    attr_index = mi.index(max(mi))
    return maxvalue, attr_index

def reset(data,attr_index):
    tmp1 = []
    tmp2 = []
    # add the attribute name to tmp1 and tmp2
    for i in range(0, len(data)):
        if data[i][attr_index] == '1':
            tmp1.append(data[i])
        else:
            tmp2.append(data[i])

    for row1 in tmp1:
        row1.pop(attr_index)

    for row2 in tmp2:
        row2.pop(attr_index)

    return tmp1, tmp2

def majorityvote(data):
    right = 0
    wrong = 0
    for i in range(0, len(data)):
        if data[i][-1] == data[0][-1]:
            right += 1
            label1 = data[i][-1]
        else:
            wrong += 1
            label2 = data[i][-1]
    if right > wrong:
        return label1
    else:
        return label2


def treebuilder(node, maxdepth, currentdepth, attr):

    if maxdepth == 0:
        node.attrvalue = majorityvote(node.data)
        return

    if len(node.data[0]) == 1:
        node.attrvalue = majorityvote(node.data)
        return
    else:
        numberlist = loadData(node.data)
        value, index = muturalinformation(numberlist)
        if (value == 0) or ((currentdepth+1) > maxdepth):
            node.attrvalue = majorityvote(node.data)
            return
        else:
            node.attrvalue = attr[index]
            currentdepth += 1
            nextkeep = attr
            attr.pop(index)
            newdata1, newdata2 = reset(node.data, index)
            node.left = Node(newdata1, None, None, None)
            attr = copy.deepcopy(nextkeep)
            treebuilder(node.left, maxdepth, currentdepth, attr)
            node.right = Node(newdata2, None, None, None)
            attr = copy.deepcopy(nextkeep)
            treebuilder(node.right, maxdepth, currentdepth, attr)
            return


def test(attr, node, testdata, list):
    if node.left == None:
        list.append(node.attrvalue)
        return
    else:
        index = attr.index(node.attrvalue)
        if testdata[index] == '1':
            return test(attr, node.left, testdata, list)
        else:
            return test(attr, node.right, testdata, list)



# main

trainfile = sys.argv[1]
testfile = sys.argv[2]
inputdepth = sys.argv[3]
trainoutput = sys.argv[4]
testoutput = sys.argv[5]
error = sys.argv[6]


# train tree
with open(trainfile, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    savedata = [row for row in reader]

attribute = savedata[0]  # save the attribute title
row = savedata[1:]  # remove the attribute title

rowlist = [[] for i in range(len(row))]
for i in range(0, len(row[0])):
    for j in range(0, len(row)):
        if row[j][i] == row[0][i]:
            rowlist[j].append("1")
        else:
            rowlist[j].append("0")



# test train_data
with open(trainfile, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    traintestdata = [row for row in reader]

attr_traintest = traintestdata[0]  # save the attribute title
row_traintest = traintestdata[1:]
traindata_length = len(row_traintest)

# find out what 0 and 1 stands for
one = row_traintest[0][-1]
for i in range(0, len(row_traintest)):
    if row_traintest[i][-1] != one:
        zero = row[i][-1]
        break
print(one, zero)

row_traintestlist = [[] for i in range(len(row_traintest))]
for i in range(0, len(row_traintest[0])):
    for j in range(0, len(row_traintest)):
        if row_traintest[j][i] == row_traintest[0][i]:
            row_traintestlist[j].append("1")
        else:
            row_traintestlist[j].append("0")


# call Node
depth = int(inputdepth)
T = Node(rowlist, None, None, None)
treebuilder(T, depth, 0, attribute)


trainerror_num = 0
trainlabellist = []
for i in range(len(row_traintestlist)):
    output = test(attr_traintest, T, row_traintestlist[i], trainlabellist)
for i in range(len(trainlabellist)):
    if trainlabellist[i] != row_traintestlist[i][-1]:
        trainerror_num += 1

# change the 0,1 number to attribute name
train_attributelist = []
for i in range(len(trainlabellist)):
    if trainlabellist[i] == '1':
        train_attributelist.append(one)
    else:
        train_attributelist.append(zero)


# write the ouput of train label
trainoutputfile = open(trainoutput, "w")
for i in range(len(trainlabellist)):
    trainoutputfile.write(train_attributelist[i]+'\n')

print('error(train):', trainerror_num/traindata_length)


# test tree
with open(testfile, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    testdata = [row for row in reader]

attr_testdata = testdata[0]
row_testdata = testdata[1:]
testdata_length = len(row_testdata)

row_testdatalist = [[] for i in range(len(row_testdata))]
for i in range(0, len(row_testdata[0])):
    for j in range(0, len(row_testdata)):
        if row_testdata[j][i] == row_traintest[0][i]:
            row_testdatalist[j].append("1")
        else:
            row_testdatalist[j].append("0")


testerror_num = 0
testlabellist = []
for i in range(len(row_testdatalist)):
    output = test(attr_testdata, T, row_testdatalist[i], testlabellist)
for i in range(len(testlabellist)):
    if testlabellist[i] != row_testdatalist[i][-1]:
        testerror_num += 1


# change the 0,1 number to attribute name
test_attributelist = []
for i in range(len(testlabellist)):
    if testlabellist[i] == '1':
        test_attributelist.append(one)
    else:
        test_attributelist.append(zero)

# write the ouput of train label
testoutputfile = open(testoutput, "w")
for i in range(len(testlabellist)):
    testoutputfile.write(test_attributelist[i]+'\n')

print('error(test):', testerror_num/testdata_length)


#error
errorrate = open(error, "w")
errorrate.write('error(train):' + str(trainerror_num/traindata_length)+'\n')
errorrate.write('error(test):' + str(testerror_num/testdata_length))

