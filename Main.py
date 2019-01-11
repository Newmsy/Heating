import HeatFlowMethods
import argparse
import matplotlib.pyplot as plt

def GetArgs():
    parse = argparse.ArgumentParser(
        description='Arguments parsed into the command line to modify variables')
    parse.add_argument('--iternum',type=int,default=2e6)
    return parse.parse_args()

if __name__ == '__main__':
    KConductivity=15 #wm^-1K^-1
    Current=12 #(Amps)
    I2pdl=(Current**2)*6.90e-7*0.001**2
    WidthList = [1.35e-6, 3.49e-6, 2.7e-6]
    LenList = [30,30,20]
    ZeroLocs=[0,79]
    WidLens = []
    for n,length in enumerate(LenList):
        for i in range(length):
            WidLens.append(WidthList[n])

    ReturnedCountNum=[1000,1e4,1e5,5e5,1e6,2e6,3e6,4e6,5e6]
    Arr=HeatFlowMethods.ArrayMaker(sum(LenList),WidLens,ZeroLocs)
    Times=int(GetArgs().iternum)
    TempReturns=HeatFlowMethods.MainIterator(Times,Arr[0],Arr[1],Arr[2],I2pdl,KConductivity,ReturnedCountNum)

    for j in range(len(TempReturns)):
        for i in range(len(TempReturns[0])):
            TempReturns[j][i]=HeatFlowMethods.EnergToTemp(TempReturns[j][i],Arr[1][i],0.001)


    for n,YVals in enumerate(TempReturns):
        plt.plot(range(sum(LenList)), YVals, label='{:.0e} timesteps'.format(int(ReturnedCountNum[n])))


    plt.legend(loc='best')
    plt.xlabel('x axis /mm')
    plt.ylabel('Temp above room temp /kelvin')
    plt.show()
