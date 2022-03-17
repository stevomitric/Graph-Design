#
# biblioteka za 2d geometriju
#
import math

def pomeriTacku(A, B, d):
    ''' Vraca koordinate tacke koja je pomerana od tacke A do tacke B duz prave koje ove dve tacke cine '''
    alpha = math.atan2(B[1]-A[1], B[0]-A[0])
    ax = d*math.cos(alpha)
    ay = d*math.sin(alpha)
    return (A[0]+ax, A[1]+ay)

def dist(A, B):
    ''' Udaljenost izmedju tacaka'''
    return ( (A[0]-B[0])**2 + (A[1]-B[1])**2 )**0.5

def nadjiCentar(A, B):
    ''' Vraca koordinate tacke koja je u centru duzi [AB] '''
    return pomeriTacku(A,B,dist(A,B)/2)

def nadjiNormalu(A, B, d):
    alpha = math.atan2(B[1]-A[1],B[0]-A[0])
    beta = math.pi/2 - alpha
    return (A[0] + d*math.cos(beta), A[1]-d*math.sin(beta) )