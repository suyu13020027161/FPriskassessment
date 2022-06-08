'''
判断线段是否相交
'''
from matplotlib import pyplot as plt
success = {
        'color':  'darkgreen',
        'size': 16,
        }

failure = {
'color':  'darkred',
'size': 16,
}

class Point:
    def get(self,text):
        self.text=text
        self.x,self.y=list(map(float,input("Enter x,y co-ordinate of point "+self.text+" :").split()))

    def plot(self):
        plt.scatter(self.x,self.y) 
        plt.text(self.x,self.y,self.text)       

def liesOnSegment(p, q, r):
    if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and 
           (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
  
def checkOrientation(p, q, r):      
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0

def checkIntersection(p1,q1,p2,q2):
    global intersectionresult
    global proper
    o1 = checkOrientation(p1, q1, p2)
    o2 = checkOrientation(p1, q1, q2)
    o3 = checkOrientation(p2, q2, p1)
    o4 = checkOrientation(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        if(o1==0 or o2==0 or o3==0 or o4==0):
            intersectionresult=True
            proper=False
        else:
            intersectionresult=True
            proper=True
        return True
    if ((o1 == 0) and liesOnSegment(p1, p2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o2 == 0) and liesOnSegment(p1, q2, q1)):
        intersectionresult=True
        proper=False
        return True
    if ((o3 == 0) and liesOnSegment(p2, p1, q2)):
        intersectionresult=True
        proper=False
        return True
    if ((o4 == 0) and liesOnSegment(p2, q1, q2)):
        intersectionresult=True
        proper=False
        return True

    intersectionresult=False
    proper=None
    return False

p1=Point()
q1=Point()
p2=Point()
q2=Point()
pointlist=[p1,q1,p2,q2]

for p in pointlist:
    pointname=[key for key,value in locals().items() if value==p]
    p.get(str(pointname[0]))
    p.plot()

checkIntersection(p1, q1, p2, q2)

plt.plot([p1.x,q1.x],[p1.y,q1.y])
plt.plot([p2.x,q2.x],[p2.y,q2.y])
if(intersectionresult==True):
    plt.xlabel("Line Segments Intersect",success)
    if(proper==True):
        plt.ylabel("Proper Intersection",success)
    else:
        plt.ylabel("Improper Intersection",failure)
else:
    plt.xlabel("Line Segments do not Intersect",failure)

plt.show()
