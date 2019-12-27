from SW_global import *
global x_with_bez,y_with_bez,x_without_bez,y_without_bez
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> Press Function <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
x_with_bez.clear()
y_with_bez.clear()
x_without_bez.clear()
y_without_bez.clear()
def font_check(x,y):
    global x_with_bez,y_with_bez,x_without_bez,y_without_bez
    NT = float
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    #plt.figure(figsize=[1,4])
    import bezier as bezier1
    # class Point
    class Point:
        def __init__(self, x = 0.0, y = 0.0):
            self.x = x
            self.y = y
            
        def distance(self, p):
            return sqrt((p.x-self.x)*(p.x-self.x)+(p.y-self.y)*(p.y-self.y))

        def length(self):
            return self.distance(Point(NT(0), NT(0)))

        def __sub__(self, p):
            return Point(self.x-p.x, self.y-p.y)

        def __add__(self, p):
            return Point(self.x+p.x, self.y+p.y)

        def __mul__(self, c):
            return Point(c*self.x, c*self.y)

        def __eq__(self, p):
            return self.x == p.x and self.y == p.y

        def __ne__(self, p):
            return not (self == p)
            
        def towards(self, target, t):
            if t == 0.5:
                return self.halfway(target)
            else:
                return Point((1.0-t)*self.x+t*target.x, (1.0-t)*self.y+t*target.y)
            
        def halfway(self, target):
            return Point((self.x+target.x).div2(), (self.y+target.y).div2())

        def compare_lex(self, p):
            if self.x < p.x:
                return -1
            if self.x > p.x:
                return 1
            if self.y < p.y:
                return -1
            if self.y > p.y:
                return 1
            return 0

        def less_lex(self, p):
            return self.compare_lex(p) < 0

        def less_eq_lex(self, p):
            return self.compare_lex(p) <= 0
            
        def __repr__(self):
            return "Point(%s, %s)" % (self.x, self.y)      

    def orientation2d(a, b, c):
        d1 = (a.x - b.x) * (a.y - c.y)
        d2 = (a.y - b.y) * (a.x - c.x)
        if d1 == d2:
            return 0
        elif d1 > d2:
            return 1
        else:
            return -1

    def leftTurn(a, b, c):
        return orientation2d(a, b, c) > 0

    def rightTurn(a, b, c):
        return orientation2d(a, b, c) < 0

    def betweenVar(a, b, c):
        return (a.x-b.x)*(c.x-b.x)+(a.y-b.y)*(c.y-b.y)<0

    class Dim:
        def __init__(self, vp):
            self.n = len(vp)
            self.vp = vp
            self.isConvex = False
            self.diam = 0
            
        def convexify(self):
            pass

        def diameter():
            if self.diam == 0:
                self.xmin = self.vp[0].x
                self.xmax = self.xmin
                self.ymin = self.vp[0].y
                self.ymax = self.ymin
                for p in self.vp:
                    if p.x < self.xmin:
                        self.xmin = p.x
                    if p.x > self.xmax:
                        self.xmax = p.x
                    if p.y < self.ymin:
                        self.ymin = p.y
                    if p.y > self.ymax:
                        self.ymax = p.y
                self.diam = min(xmax-xmin, ymax-ymin)
            

    class Bezier(Dim):
        def __init__(self, v):
            self.deg = len(v) - 1
            self.cp = v
            self.tmin = NT(0)
            self.tmax = NT(1)
          
        def getPoint(self, t):
            curr = [0]*self.deg
            # get initial
            for i in range(self.deg):
                curr[i] = self.cp[i].towards(self.cp[i+1], t)
            for i in range(self.deg-1):
                for j in range(self.deg-1-i):
                    curr[j] = curr[j].towards(curr[j+1], t)
            return curr[0]

        def subdivision(self, t):
            lseq = [0]*(self.deg+1)
            rseq = [0]*(self.deg+1)
            curr = [0.0]*self.deg

            lseq[0] = self.cp[0]
            rseq[self.deg] = self.cp[self.deg]
            for i in range(self.deg):
                curr[i] = self.cp[i].towards(self.cp[i+1], t)
            for i in range(self.deg-1):
                lseq[i+1] = curr[0]
                rseq[self.deg-i-1] = curr[self.deg-i-1]
                for j in range(self.deg-1-i):
                    curr[j] = curr[j].towards(curr[j+1], t)
                    lseq[self.deg] = curr[0]
                    rseq[0] = curr[0]  
            return [lseq, rseq]

    def plotCP(cp):
        x = []; y = []
        for i in range(len(cp)):
            x.append(cp[i].x)
            y.append(cp[i].y)
        plot(x, y)
            
    def plotBezier(bezier, n):
        global x_with_bez,y_with_bez
        eps = NT(1)/n
        x = []
        y = []
            
        t = 0
        for i in range(n+1):
            p = bezier.getPoint(t)
            t = t + eps
            x.append(p.x)
            y.append(p.y)
            #plt.plot(x, y,color="b")
        x_with_bez.append(x)
        y_with_bez.append(y)

    def pt(x, y):
        return Point(NT(x), NT(y))
           
    def Slp(x,y):
        try:
            z = (y[i+1]-y[i])/(x[i+1]-x[i])
        except:
            z = 0
        return z
    def angle(x,y):
            pass

    import numpy as np
    def FinalCall(x,y):
        vp=[]
        for pnt in range(len(x)):
            vp.append(pt(x[pnt],y[pnt]))
        bc = Bezier(vp)
        [left, right] = bc.subdivision(0.4)
        # plot left
        plotBezier(Bezier(left), 100)
           
        # plot left
        plotBezier(Bezier(right), 100)
        plt.plot(x1x,x1y)
    # Get angle of three lines
    ######################################################################################################################
    def angle(x,y):
        def ang(pt1x,pt1y,pt2x,pt2y,pt3x,pt3y):
            a = np.array([pt1x,pt1y])
            b = np.array([pt2x,pt2y])
            c = np.array([pt3x,pt3y])

            ba = a - b
            bc = c - b

            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)
            return np.degrees(angle)
        lnt=len(x)
        i=0
        x1x=[]
        x1y=[]
        x2x=[]
        x2y=[]
          
        while True:
            if i==(lnt-2):
                break
            else:
                pt1x=x[i]
                pt1y=y[i]
                pt2x=x[i+1]
                pt2y=y[i+1]
                pt3x=x[i+2]
                pt3y=y[i+2]
                z= ang(pt1x,pt1y,pt2x,pt2y,pt3x,pt3y)
                if int(z)<=90.0:
                    x1x.append(pt1x)
                    x1x.append(pt2x)
                    x1x.append(pt3x)
                    x1y.append(pt1y)
                    x1y.append(pt2y)
                    x1y.append(pt3y)
                else:
                    x2x.append(pt1x)
                    x2x.append(pt2x)
                    x2x.append(pt3x)
                    x2y.append(pt1y)
                    x2y.append(pt2y)
                    x2y.append(pt3y)
                i+=1
        return x1x,x1y,x2x,x2y
    def excp(x,y):
        ax= plt.axes()
        if isinstance(x[0],list):
            for i in range(len(x)):
                nodes = np.asarray([x[i],y[i]],dtype=np.double)
                curve = bezier1.Curve(nodes, degree=2)
                curve.plot(num_pts=100,ax=ax)
            #plt.show()
        else:
            nodes = np.asarray([x,y],dtype=np.cdouble)
            curve = bezier1.Curve(nodes, degree=2)
            curve.plot(num_pts=100,ax=ax)
    ingr_list=("%","@",";")
    try:
        if False:
            excp(x,y)
        else:
            if isinstance(x[0],list):
                for ij in range(len(x)):
                    if len(x[ij])>=3:
                        x1x,x1y,x2x,x2y=angle(x[ij],y[ij])
                        x_without_bez.append(x1x)
                        y_without_bez.append(x1y)
                        FinalCall(x2x,x2y)
                    else:
                        x_without_bez.append(x[ij])
                        y_without_bez.append(y[ij])
            else:
                if len(x)>=3:
                    x1x,x1y,x2x,x2y=angle(x,y)
                    x_without_bez.append(x1x)
                    y_without_bez.append(x1y)
                    FinalCall(x2x,x2y)
                else:
                    x_without_bez.append(x)
                    y_without_bez.append(y)
    except Exception as e:
        if isinstance(x[0],list):
            x_without_bez.append(x)
            y_without_bez.append(y)
        else:
            x_without_bez.append(x)
            y_without_bez.append(y)
    c1g=[]
    c2g=[]
    for i in range(len(x_with_bez)):
        c1g.append(x_with_bez[i])
        c2g.append(y_with_bez[i])
    for lk in range(len(x_without_bez)):
        c1g.append(x_without_bez[lk])
        c2g.append(y_without_bez[lk])
    y_without_bez=[]
    x_without_bez=[]
    x_with_bez=[]
    y_with_bez=[]
    return c1g,c2g