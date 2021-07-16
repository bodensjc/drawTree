from vpython import*
import random

#initial parameters
split=5
rounds=4
maxradius=1
radius=0.3
maxAttempts=1000
delta = 0.1

pairlst=[]#empty list to store endpoints of all branches


#greate graph environment
circGraph= graph(width=1000, height=1000,
    xmin=-1.1, xmax=1.1, ymin=-1.1, ymax=1.1,
    title="Tree Program", xtitle=f"split = {split}\t maxradius = {maxradius}\t length = {radius}\t rounds = {rounds}")


#circle/origin setup
f1 = gcurve(color=color.cyan)
for theta in arange(0, 2*pi, 0.01):
    f1.plot(maxradius*cos(theta),maxradius*sin(theta))
finit = gdots(color=color.red)
finit.plot([0,0])

#variable for randomized angle
def randomAng_func():
    return 2*pi*(random.random()) 

#check if new branch intersects with any existing branch
def checkIntersect(newBranch):
    global int_seg
    if len(pairlst)<split:
        return True
    X1=newBranch[0][0]
    Y1=newBranch[0][1]
    X2=newBranch[1][0]
    Y2=newBranch[1][1]
    
    #exit immediately if it is outside of circle
    if X2**2 + Y2**2 > maxradius**2:
        return False

    #continue for intersections with other line segments
    for segment in pairlst:
        X3=segment[0][0]
        Y3=segment[0][1]
        X4=segment[1][0]
        Y4=segment[1][1]
        if (max(X1,X2) <= min(X3,X4)):
            continue  #intersection of x domains is empty set
        A1 = (Y1-Y2)/(X1-X2)  #pay attention to not dividing by zero
        A2 = (Y3-Y4)/(X3-X4)  #pay attention to not dividing by zero
        b1 = Y1-A1*X1
        b2 = Y3-A2*X3
        if (A1 == A2):
            continue  #parallel segments cannot intersect
        Xa = (b2 - b1) / (A1 - A2)   #pay attention to not dividing by zero
        if ( (Xa <= max( min(X1,X2), min(X3,X4) )) or (Xa >= min( max(X1,X2), max(X3,X4) )) ):
            continue  #intersection occurs, but is not in the domain of x values of the segment
        else:
          int_seg = segment
        return False
    return True
    
def line(p1, p2): #some special math here to determine if intersection occurs again
                A = (p1[1] - p2[1])
                B = (p2[0] - p1[0])
                C = (p1[0]*p2[1] - p2[0]*p1[1])
                return A, B, -C

def intersection(L1, L2):
                D  = L1[0] * L2[1] - L1[1] * L2[0]
                Dx = L1[2] * L2[1] - L1[1] * L2[2]
                Dy = L1[0] * L2[2] - L1[2] * L2[0]
                global Xo
                global Yo
                if D != 0:
                  Xi = Dx / D
                  Yi = Dy / D
                  return sqrt((Xi-Xo)**2+(Yi-Yo)**2) #return distance of intersection segment
                else:
                  return False
                


def branch(origin):
    global int_seg
    global Xo
    global Yo
    global roundNumber
    Xo, Yo = origin
    tmplst=[] #for output
    scale = 1 - roundNumber/(rounds+1)
    for i in range(split):
        theta = randomAng_func() #choose angle randomly
        for k in range(maxAttempts):
            target=[scale*radius*cos(theta)+Xo,scale*radius*sin(theta)+Yo] #create target point 
            if checkIntersect([origin,target]): #if it is okay, draw it and move on. otherwise try again
                gcurve(markers=False, width=3*scale, color = color.black).plot([origin,target])
                tmplst.append(target)
                pairlst.append([origin,target])
                print(f'round {roundNumber}, node {nodeNumber}, segment {i+1} drawn')
                #scale=1
                break
            else:
                theta += delta #move slightly
        else: #if it doesn't work for all angles
            #JULIE KEEP WORKING HERE
            L1 = line(origin, target) #new branch
            print(int_seg)
            L2 = line(int_seg[0],int_seg[1])
            length = intersection(L1,L2)
            scale=scale*length*0.5 #to intersection point and divides it in half, and sets number as the new scale
            target=[scale*radius*cos(theta)+Xo,scale*radius*sin(theta)+Yo]
            gcurve(markers=False, width=3*scale, color = color.black).plot([origin,target])
            tmplst.append(target)
            pairlst.append([origin,target])
            print(f'round {roundNumber}, node {nodeNumber}, segment {i+1} drawn')
            continue
    return tmplst #return list of new endpoints from this origin



def drawTree(currentRound, originLst):
    if currentRound==0:
        print('Drawing complete.')
        return None
    else:
        global roundNumber
        global nodeNumber
        roundNumber = rounds - currentRound+1
        nodeNumber = 0
        tmp=[]
        for point in originLst:
            tmp += branch(point)
            nodeNumber += 1
        drawTree(currentRound-1, tmp)



drawTree(rounds, [[0,0]])