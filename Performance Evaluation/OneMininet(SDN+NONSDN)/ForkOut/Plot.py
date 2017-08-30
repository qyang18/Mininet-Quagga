
import numpy as np
import matplotlib.pyplot as plt

# def getLogFile(filename):
#     # filename='log1'
#     f=open(filename, 'r')
#     data=[]
#     counter=1
#
#     for line in f:
#         counter+=1
#         if counter >= 8:
#             if line[0] != '[':
#                 break
#             # print([line.split('  ')[2],line.split('  ')[4]])
#             data.append([line.split('  ')[2],line.split('  ')[4]])
#     return data

def getLogFile(filename):
    # filename='log1'
    f=open(filename, 'r')
    data=[]
    counter=1

    for line in f:
        counter+=1
        segments = line.split(' ')

        if counter >= 8:
            if line[0] != '[':
                break
            # print(line.split('  '))
            # data.append([line.split('  ')[2],line.split('  ')[5]])
            #print(segments)
            # print(line.split(' '));
            print(segments)
            if "bits/sec" in segments:
                i = segments.index("bits/sec")
                data.append([''] + dealWithUnit(segments[i-1]+' '+segments[i]))
            elif "Kbits/sec" in segments:
                i = segments.index("Kbits/sec")
                data.append([''] + dealWithUnit(segments[i - 1] + ' ' + segments[i]))
                # data.append([segments[i - 2], segments[i - 1], segments[i]])
            elif "Mbits/sec" in segments:
                i = segments.index("Mbits/sec")
                data.append([''] + dealWithUnit(segments[i - 1] + ' ' + segments[i]))
                # data.append([segments[i - 2], segments[i - 1], segments[i]])
            # data.append([segments[2]] + dealWithUnit(segments[4]))
    if data!=[]:
        data.pop()
    print('data')
    print(data)
    return data

def getLogFileInCDF(filename):
    # filename='log1'
    f=open(filename, 'r')
    data=[]
    counter=1

    for line in f:
        counter+=1

        segments=line.split('  ')

        if counter == 8:
            data.append([segments[2]] + dealWithUnit(segments[4]))

        if counter >= 9:
            if line[0] != '[':
                break
            data.append([segments[2]] + [(data[counter - 9][1] + dealWithUnit(segments[4])[0])] + [(dealWithUnit(segments[4])[1])])

    print(data)
    return data

def dealWithUnit(line):
    temp=line.split(' ')
    value=float(temp[-2])

    unit=temp[-1]
    if ('Mbits' in unit) or ('MBytes' in unit):
        pass
    elif ('Kbits' in unit) or ('KBytes' in unit):
        value=value/1000
    elif ('bits' in unit) or ('Bytes' in unit):
        value=value/1000000

    return [value,unit]

def plot(plt,file,start,end,color,name,timeinterval):
    data = []
    maxColumn=0
    for i in range(0,end-start+1):
        maxColumn=max([len(file[i]),maxColumn])
    print('max Column='+str(maxColumn))

    time = np.linspace(0, maxColumn*timeinterval, maxColumn)
    for i in range(0,maxColumn):
        tempData=0
        for eachfile in file:
            #get line i and add up together
            try:
                tempData+=eachfile[i][1]
            except:
                tempData+=0
                # tempData+=eachfile[len(eachfile)-1][1]
        data.append(tempData)

    # plt.title('Plot of Two Way Test With Pi as Host in Hybrid mode')
    plt.xlabel('time')
    plt.ylabel('Aggregate Throughput')

    #print(time)
    for i, each in enumerate(data): print i, each
    #plt.scatter(time,data)
    plt.plot(time, data, c=color, label=name)



    # baselinetime=np.linspace(0,maxColumn,maxColumn)
    # baselinedata=np.linspace(0,data[len(data)-1],maxColumn)
    # plt.plot(baselinetime, baselinedata)
    #plt.show()

if __name__ == "__main__":
    # file=getLogFile('log1')
    # print(file)
    file1=[]
    file2=[]
    file3=[]
    p = plt
    p.title('Plot of Fork-out Test With Quagga Router in One Mininet mode')
    # p.figure(1)
    # for i in range(1,4):
    #     file1.append(getLogFile('./ForkInTestServerThread'+str(i)+'.log'))
    #     plot(p, file1, 1, 1, 'r', 'H'+str(i), 1)
    file1.append(getLogFile('./ForkOutTestServerThread1.log'))
    plot(p, file1, 1, 1, 'r', 'H1', 1)

    file2.append(getLogFile('./ForkOutTestServerThread2.log'))
    plot(p, file2, 1, 1, 'g', 'H2', 1)

    file3.append(getLogFile('./ForkOutTestServerThread3.log'))
    plot(p, file3, 1, 1, 'b', 'H3', 1)

    p.legend(loc='lower right')
    p.show()