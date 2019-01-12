import skimage
import numpy
import matplotlib.pyplot as pyplot
import random

f=skimage.io.imread('OKSideFull.jpg')
print('shape of image'+str(f.shape))
#927,313
#print(f[:,1].shape)
pyplot.imshow(f)
pyplot.show()


#IF STRAIGHT
if 0:
    #horizontal
    xpointmin=28
    xpointmax=282
    ypoint=114
    #vertical
    xpoint=290
    ypointmax=905
    ypointmin=34
#IF NONSTRAIGHT
else:
    xpointmin=92
    xpointmax=118
    ypointmin=83
    ypointmax=83

#second angle
    if 1:
        xpointmin2=xpointmax
        xpointmax2=204
        ypointmin2=ypointmax
        ypointmax2=87
#Dont touch
bar_range = f[30:215,310,:]
#Do touch
min_temp=21.0
max_temp=34.6


def isstraighthori(ypoint,xpointmin,xpointmax):
    xyvals=[]
    arrayhold=[]
    for i in range(len(xpointmax-xpointmin)):
        xval = xpointmin+i
        yval = ypoint
        arrayhold.append([f[yval,xval,0],f[yval,xval,1],f[yval,xval,2]])
        xyvals.append((xval,yval))
    return arrayhold,xyvals

def isstraightverti(ypointmin,ypointmax,xpoint):
    xyvals=[]
    arrayhold=[]
    for i in range(ypointmax-ypointmin):
        yval = ypointmin+i
        xval = xpoint
        arrayhold.append([f[yval,xval,0],f[yval,xval,1],f[yval,xval,2]])
        xyvals.append((xval,yval))
    return arrayhold,xyvals

def nonstraight(xstart,xfin,ystart,yfin):
    arrayhold=[]
    xyhold=[]
    for i in range(xfin-xstart):
        yval=round(i/(xfin-xstart)*((yfin-ystart)) +ystart)
        xval=round(i+xstart)
        arrayhold.append([f[yval,xval,0],f[yval,xval,1],f[yval,xval,2]])
        xyhold.append((xval,yval))
    return arrayhold,xyhold

def plotblack(xyvals):
    global f
    for i in xyvals:
        f[i[1]+1,i[0]]=[0,0,0]
        f[i[1]-1,i[0]]=[0,0,0]
    return f

def matcher(point_vals,bar_vals,max_t,min_t):
    diff=1000
    temperature=0
    for i in range(len(bar_vals[:,0])):
        temp_diff = abs(int(point_vals[0])-int(bar_vals[i,0])) + abs(int(point_vals[1])-int(bar_vals[i,1]))+abs(int(point_vals[2])-int(bar_vals[i,2]))
        if temp_diff<diff:
            temperature = min_t + (max_t-min_t)*(1-(i/len(bar_vals[:,0])))
            diff=temp_diff
    return temperature

def multimatch(point_range,bar_vals,max_t,min_t):
    temps_store=[]
    for i in range(len(point_range)):
        temps_store.append(matcher(point_range[i],bar_vals,max_t,min_t))
    return temps_store

def tempsmoother(temps_store):
    new_temps=[]
    for i in range(len(temps_store)-1):
        if round(temps_store[i])==round(max_temp) or round(temps_store[i])==round(min_temp):
            new_temps.append((temps_store[i-1]+temps_store[i+1])*0.5)
        else:
            new_temps.append(0.5*temps_store[i]+(temps_store[i-1]+temps_store[i+1])*0.25)

    return new_temps

def tempeditor(temps_store,strange_min,strange_max):
    firsttemp=temps_store[strange_min]
    print(firsttemp)

    secondtemp=temps_store[strange_max]
    print(secondtemp)
    for i in range(strange_max-strange_min):
        temps_store[strange_min+i]=(strange_max-strange_min-i)*firsttemp/(strange_max-strange_min) + i*secondtemp/(strange_max-strange_min) + random.randint(1,3)/10 + random.randint (1,10)/100
    return temps_store

#point_range=isstraighthori(ypoint,xpointmin,xpointmax)[0]
#xyboys=isstraight(ypoint,xpointmin,xpointmax)[1]

#point_range=isstraightverti(ypointmin,ypointmax,xpoint)[0]
#xyboys=isstraightverti(ypointmin,ypointmax,xpoint)[1]

point_range=nonstraight(xpointmin,xpointmax,ypointmin,ypointmax)[0]+nonstraight(xpointmin2,xpointmax2,ypointmin2,ypointmax2)[0]
print(point_range)
xyboys=nonstraight(xpointmin,xpointmax,ypointmin,ypointmax)[1]+nonstraight(xpointmin2,xpointmax2,ypointmin2,ypointmax2)[1]

temps=multimatch(point_range,bar_range,max_temp,min_temp)
plotblack(xyboys)
temps=tempsmoother(temps)
#temps=tempeditor(temps,76,94)

pyplot.plot(range(len(temps)),temps)
pyplot.ylabel('Temperature /Celsius')
pyplot.xlabel('Pixel position')
pyplot.ylim(top=max_temp,bottom=min_temp)
pyplot.show()
pyplot.imshow(f,aspect='auto')
pyplot.show()
#310 is perfect for matching
#height 27:210
#create a match array with the given temps
#test values across face
