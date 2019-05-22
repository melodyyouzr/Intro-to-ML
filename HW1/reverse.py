import sys

infile = sys.argv[1]
outfile = sys.argv[2]


file1 = open(infile,"r")
lines = file1.readlines()

lines.reverse()
file2 = open(outfile,"w")

for eachline in lines:
	file2.write(eachline)

file1.close()
file2.close()



	
