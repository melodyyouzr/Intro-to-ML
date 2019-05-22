
import sys
import csv
from math import log

infile = sys.argv[1]
outfile = sys.argv[2]

file2 = open(outfile, "w")

with open(infile, 'rt') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[-1] for row in reader]

new_column = column[1:]

num = 0
for s in new_column:
    if s == new_column[0]:
        num += 1

if num != 0:
    entropy1 = -(num/len(new_column)) * (log(num/len(new_column), 2))
else:
    entropy1 = 0

if len(new_column)-num != 0:
    entropy2 = - ((len(new_column)-num)/len(new_column)) * log((len(new_column)-num)/len(new_column), 2)
else:
    entropy2 = 0

entropy = entropy1 + entropy2


if num >= len(new_column)-num:
    error_rate = (len(new_column)-num)/len(new_column)
else:
    error_rate = num/len(new_column)

file2.write('entropy: ' + str(entropy) + '\n')
file2.write('error: ' + str(error_rate))

csvfile.close()
file2.close()

