import matplotlib.pyplot as pyplot


def ArrayMaker(dls,Area,SinkLocs):
    DlVals=list(0 for i in range(dls))
    if len(Area)!=dls:
        return
    print(DlVals)
    print(Area)
    print(SinkLocs)
    return DlVals,Area,SinkLocs

def SinkSetter(SinkLocs,DlVals):
    for Loc in SinkLocs:
        DlVals[Loc]=0
    return DlVals

def MainIterator(Times, DlVals, Area,SinkLocs,I2pdl,KConductivity,ReturnedCountNum):
    ReturnedCounts=[]
    for Time in range(Times):
        if Time in ReturnedCountNum:
            ReturnedCounts.append(DlVals)
        #DlVals = list(i+ConstAdd for i in DlVals)
        for i in range(len(Area)):
            DlVals[i]+=I2pdl/Area[i]

        DlVals= SinkSetter(SinkLocs,DlVals)
        #DiffList is in Temps, DlVals is in Joules
        DiffList=[]
        for i in range(len(DlVals)-1):
            DiffList.append(EnergToTemp(DlVals[i],Area[i],0.001)-EnergToTemp(DlVals[i+1],Area[i+1],0.001))
        #print('2')
        #print(DiffList)
        NewDlVals=[]
        NewDlVals.append(DlVals[0]-Area[0]*DiffList[0]*KConductivity)
        for i in range(len(DlVals)-2):

            NewDlVals.append(DlVals[i+1]+Area[i]*DiffList[i]*KConductivity-Area[i]*DiffList[i+1]*KConductivity)
        NewDlVals.append(DlVals[-1]+Area[-1]*DiffList[-1]*KConductivity)
        DlVals=NewDlVals
    TotalReturn=[]

    for i in ReturnedCounts:
        TotalReturn.append(i)
    TotalReturn.append(DlVals)
    return TotalReturn

def EnergToTemp(Energy, Area, dl):
    #These values only work for stainless steel, redefine for other materials
    return Energy/(502*Area*dl*7700)

def TempToEnerg(Temp, Area, dl):
    #These values only work for stainless steel, redefine for other materials
    return (502*Area*dl*7700*Temp)


if __name__ == '__main__':
    KConductivity=15 #wm^-1K^-1
    Current=12 #(Amps)

    I2pdl=(Current**2)*6.90e-7*0.001**2
    Arr=ArrayMaker(80,list(1.35e-6 for i in range(30))+list(3.49e-6 for i in range(30))+list(2.7e-6 for i in range(20)),[0,79])
    a=MainIterator(2000000,Arr[0],Arr[1],Arr[2],I2pdl,KConductivity)

    for j in range(len(a)):
        for i in range(len(a[0])):
            a[j][i]=EnergToTemp(a[j][i],Arr[1][i],0.001)


    pyplot.plot(range(len(a[0])),a[1],label='1e3 timesteps')
    pyplot.plot(range(len(a[0])),a[2],label='1e4 timesteps')
    pyplot.plot(range(len(a[0])),a[3],label='1e5 timesteps')
    #pyplot.plot(range(len(a[0])),a[4],label='5e5 timesteps')
    #pyplot.plot(range(len(a[0])),a[5],label='1e6 timesteps')
    #pyplot.plot(range(len(a[0])),a[6],label='2e6 timesteps')
    #pyplot.plot(range(len(a[0])),a[7],label='3e6 timesteps')
    #pyplot.plot(range(len(a[0])),a[8],label='4e6 timesteps')
    pyplot.plot(range(len(a[0])),a[0],label='2e6 timesteps')
    pyplot.legend(loc='best')
    pyplot.xlabel('x axis /mm')
    pyplot.ylabel('Temp above room temp /kelvin')
    pyplot.show()
