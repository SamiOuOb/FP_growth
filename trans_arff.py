f = open('data.ntrans_0.1.tlen_5.nitems_0.01', 'r')

input=f.read()
list=input.split()
#print(list)

data=[list[i:i+3] for i in range(0,len(list),3)] #list fragment
#print(data)

data2=[]
for i in range(0,len(list)/3):
    j=3*i+2
    data2.append(list[j])
# print(data2)

data3=[]
data4=[]
for i in range(1,len(list)/3):
    data3.append(data2[i-1])
    if(int(list[i*3])-int(list[(i-1)*3])==1):
        data4.append(data3)
        data3=[]
data3.append(data2[i])
data4.append(data3)
#print(data4)

f2 = open('weka_data.arff', 'w')
f2.write('@relation \'TestID\'\n')
for i in range(0,10):
    f2.write('@attribute ')
    f2.write(str(i))
    f2.write(' {F, T}\n')
f2.write('@data\n')
for i in range(0,len(data4)):
    count=0
    f2.write('{')
    for j in range(0,10):
        if str(j) in data4[i]:
            f2.write(str(j))
            f2.write(' T')
            count=count+1
            if  count < len(data4[i]):
                f2.write(', ')

            print j,'in'
    f2.write('}\n')