import skimage
import numpy
import matplotlib.pyplot as pyplot


f=skimage.io.imread('topview.png')
print(f.shape)
#927,313
print(f[:,1].shape)
pyplot.imshow(f)
pyplot.show()


#IF STRAIGHT
if 1:
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
    xpointmin=18
    xpointmax=112
    ypointmin=108
    ypointmax=91

#second angle
    if 1:
        xpointmin2=xpointmax
        xpointmax2=275
        ypointmin2=ypointmax
        ypointmax2=105
#Dont touch
bar_range = f[30:415,19,:]
#Do touch
min_temp=21.0
max_temp=30.7


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


#point_range=isstraighthori(ypoint,xpointmin,xpointmax)[0]
#xyboys=isstraight(ypoint,xpointmin,xpointmax)[1]

point_range=isstraightverti(ypointmin,ypointmax,xpoint)[0]
xyboys=isstraightverti(ypointmin,ypointmax,xpoint)[1]

#point_range=nonstraight(xpointmin,xpointmax,ypointmin,ypointmax)[0]+nonstraight(xpointmin2,xpointmax2,ypointmin2,ypointmax2)[0]
print(point_range)
#xyboys=nonstraight(xpointmin,xpointmax,ypointmin,ypointmax)[1]+nonstraight(xpointmin2,xpointmax2,ypointmin2,ypointmax2)[1]

temps=multimatch(point_range,bar_range,max_temp,min_temp)
plotblack(xyboys)
pyplot.plot(range(len(temps)),temps)
pyplot.ylabel('Temperature /Celsius')
pyplot.xlabel('Pixel position')
pyplot.show()
pyplot.imshow(f,aspect='auto')
pyplot.show()
#310 is perfect for matching
#height 27:210
#create a match array with the given temps
#test values across face
