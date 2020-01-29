def blintersection((x1,y1),(x2,y2)):
    """Takes two tuples and finds the intersection point from bottom left which is the combination
    of biggest x and biggest y 
    """
    if x1>=x2:
        m1=x1
    else:
        m1=x2
    
    if y1>=y2:
        m2=y1
    else:
        m2=y2
    return (m1,m2)
def trintersection((x1,y1),(x2,y2)):
    """Takes two tuples and finds the intersection point from top right which is the combination
    of least x and least y 
    """
    if x1>=x2:
        m1=x2
    else:
        m1=x1
        
    if y1>=y2:
        m2=y2
    else:
        m2=y1
    return (m1,m2)
def insiderect((t1bl,t1tr),(t2bl,t2tr)):
    """Gets the tuple pairs that defines two rectangles and returns the intersection of the two rectangles"""
    return(blintersection(t1bl,t2bl), trintersection(t1tr,t2tr))
def surfacearea((tbl,ttr)):
    deltax=ttr[0]-tbl[0]
    deltay=ttr[1]-tbl[1]
    if deltax < 0 or deltay < 0:
        return 0 #handles the case for disjoint rectangles
    else:
        return deltax*deltay
def isCovered(cp_bl,cp_tr,t1_bl,t1_tr,t2_bl,t2_tr):
    fintersect=insiderect((cp_bl,cp_tr),(t1_bl,t1_tr))
    secintersect=insiderect((cp_bl,cp_tr),(t2_bl,t2_tr))
    afirst=surfacearea(fintersect)
    asecond=surfacearea(secintersect)
    if afirst==0 or asecond==0:
        ainside= afirst + asecond
    else:
        insofins=insiderect(fintersect,secintersect)
        ainsofins = surfacearea(insofins)
        ainside = afirst + asecond - ainsofins
    if ainside >= surfacearea((cp_bl,cp_tr)):
        return "COMPLETELY COVERED"
    else:
        return "NOT COMPLETELY COVERED"
