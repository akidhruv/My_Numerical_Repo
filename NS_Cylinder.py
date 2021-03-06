import numpy as np
import matplotlib.pyplot as plt
from math import *


## Navier-Stokes solver for the flow over a cylinder (Staggered Grid)

# Defining Grid Parameters

Lx=1. #m
Ly=1. #m 

Nx=15
Ny=15

dx=Lx/(Nx-1)
dy=Ly/(Ny-1)

r=0.05 #m # Cylinder radius
L=2*r 

# Defining Global Constants

#mu=20.94*(10**-6) #m^2/s
mu=0.01
rho=1. #kg/m^3
Re=100
#U=(Re*mu)/L
U=1.

w=1.1 # Relaxation factor

# Staggered Grid

xstart=0
ystart=0

x=np.zeros((Nx,1),dtype=float)
y=np.zeros((Ny,1),dtype=float)

for i in range(Nx):
    x[i]=xstart+i*dx

for j in range(Ny):
    y[j]=ystart+j*dy


xp=np.zeros((Nx+1,1),dtype=float)
yp=np.zeros((Ny+1,1),dtype=float)
p=np.zeros((Nx+1,Ny+1),dtype=float)


xu=np.zeros((Nx,1),dtype=float)
yu=np.zeros((Ny+1,1),dtype=float)
u=np.zeros((Nx,Ny+1),dtype=float)
ut=np.zeros((Nx,Ny+1),dtype=float)


xv=np.zeros((Nx+1,1),dtype=float)
yv=np.zeros((Ny,1),dtype=float)
v=np.zeros((Nx+1,Ny),dtype=float)
vt=np.zeros((Nx+1,Ny),dtype=float)




for i in range(1,Nx):
    for j in range(1,Ny):
        xp[i]=(x[i-1]+x[i])/2;
        yp[j]=(y[j-1]+y[j])/2;

xp[0]=xp[1]-dx;
yp[0]=yp[1]-dy;

xp[-1]=xp[-2]+dx;
yp[-1]=yp[-2]+dy;

for i in range(Nx):
    for j in range(1,Ny):
        xu[i]=x[i]
        yu[j]=(y[j-1]+y[j])/2;

xu[0]=xu[1]-dx;
yu[0]=yu[1]-dy;

xu[-1]=xu[-2]+dx;
yu[-1]=yu[-2]+dy;


for i in range(1,Nx):
    for j in range(Ny):
        yv[j]=y[j]
        xv[i]=(x[i-1]+x[i])/2;

xv[0]=xv[1]-dx;
yv[0]=yv[1]-dy;

xv[-1]=xv[-2]+dx;
yv[-1]=yv[-2]+dy;




[X,Y]=np.meshgrid(x,y)

plt.figure(1)
plt.plot(X.T,Y.T,'g')
plt.plot(X,Y,'g')

for i in range(Nx+1):
    for j in range(Ny+1):
       plt.plot(xp[i],yp[j],'.b')

for i in range(Nx):
    for j in range(Ny+1):
       plt.plot(xu[i],yu[j],'>k')
       
for i in range(Nx+1):
    for j in range(Ny):
       plt.plot(xv[i],yv[j],'^m')



dis=np.linspace(0.,pi,20)
xcircle=0.3+r*np.cos(dis)
ycircle=np.sqrt(r**2-(xcircle-0.3)**2)

xcircle=np.concatenate([xcircle,xcircle[::-1]])
ycircle=np.concatenate([ycircle,-ycircle[::-1]])

ycircle=ycircle+0.5

#plt.plot(xcircle,ycircle,'k')
plt.axis([-0.1,1.1,-0.1,1.1])
plt.show()


iu=[]
for i in range(len(xu)):
    for j in range(len(yu)):
        if(sqrt((xu[i]-0.3)**2+(yu[j]-0.5)**2)<=r):
            iu.append([i,j])

iu=np.asarray(iu)

iv=[]
for i in range(len(xv)):
    for j in range(len(yv)):
        if(sqrt((xv[i]-0.3)**2+(yv[j]-0.5)**2)<=r):
            iv.append([i,j])
            
iv=np.asarray(iv)

bul=min(iu[:,0])
bur=max(iu[:,0])
bub=min(iu[:,1])
but=max(iu[:,1])

cux=np.linspace(bul,bur,bur-bul+1)

bu=[]

for i in range(len(cux)):
    
    ind=np.where(iu[:,0]==cux[i])
    
    Min=iu[ind[0][0]][1]
    Max=iu[ind[0][0]][1]
    
    for j in range(len(ind[0])):
        if(iu[ind[0][j]][1]<Min):
            Min=iu[ind[0][j]][1]
        if(iu[ind[0][j]][1]>Max):
            Max=iu[ind[0][j]][1]
        
    bu.append([cux[i],Min-1])
    bu.append([cux[i],Max+1])

cuy=np.linspace(bub,but,but-bub+1)

for i in range(len(cuy)):
    
    ind=np.where(iu[:,1]==cuy[i])
    
    Min=iu[ind[0][0]][0]
    Max=iu[ind[0][0]][0]
    
    for j in range(len(ind[0])):
        if(iu[ind[0][j]][0]<Min):
            Min=iu[ind[0][j]][0]
        if(iu[ind[0][j]][0]>Max):
            Max=iu[ind[0][j]][0]
    
    bu.append([Min-1,cuy[i]])
    bu.append([Max+1,cuy[i]])


bu=np.asarray(bu)

for i in range(len(bu)):
    plt.plot(xu[bu[i,0]],yu[bu[i,1]],'.b')
 



bvl=min(iv[:,0])
bvr=max(iv[:,0])
bvb=min(iv[:,1])
bvt=max(iv[:,1])

cvx=np.linspace(bvl,bvr,bvr-bvl+1)

bv=[]

for i in range(len(cvx)):
    
    ind=np.where(iv[:,0]==cvx[i])
    
    Min=iv[ind[0][0]][1]
    Max=iv[ind[0][0]][1]
    
    for j in range(len(ind[0])):
        if(iv[ind[0][j]][1]<Min):
            Min=iv[ind[0][j]][1]
        if(iv[ind[0][j]][1]>Max):
            Max=iv[ind[0][j]][1]
        
    bv.append([cvx[i],Min-1])
    bv.append([cvx[i],Max+1])

cvy=np.linspace(bvb,bvt,bvt-bvb+1)

for i in range(len(cvy)):
    
    ind=np.where(iv[:,1]==cvy[i])
    
    Min=iv[ind[0][0]][0]
    Max=iv[ind[0][0]][0]
    
    for j in range(len(ind[0])):
        if(iv[ind[0][j]][0]<Min):
            Min=iv[ind[0][j]][0]
        if(iv[ind[0][j]][0]>Max):
            Max=iv[ind[0][j]][0]
    
    bv.append([Min-1,cvy[i]])
    bv.append([Max+1,cvy[i]])


bv=np.asarray(bv)

for i in range(len(bv)):
    plt.plot(xv[bv[i,0]],yv[bv[i,1]],'xk')
    
    
# Navier Stokes Solver

# Defining functions

def F1C(ue,uw,us,un,vs,vn,dx,dy):
    F1C=-((ue**2)-(uw**2))/dx-((un*vn)-(us*vs))/dy
    return F1C

def FV(uP,uE,uW,uN,uS,dx,dy,mu):
    FV=(mu/dx)*(((uE-uP)/dx)-((uP-uW)/dx))+(mu/dy)*(((uN-uP)/dy)-((uP-uS)/dy))
    return FV

def F2C(vn,vs,ve,vw,ue,uw,dx,dy):
    F2C=-((ue*ve)-(uw*vw))/dx-((vn**2)-(vs**2))/dy
    return F2C
    
t=0
tmax=7
dt=0.45*min(dx,dy)
nt=int((tmax-t)/dt)

maxit=100
[X,Y]=np.meshgrid(x,y)

for tstep in range(nt):
    
    ue1=(u[1:-1,1:-1]+u[2:,1:-1])/2
    uw1=(u[1:-1,1:-1]+u[:-2,1:-1])/2
    us1=(u[1:-1,1:-1]+u[1:-1,:-2])/2
    un1=(u[1:-1,1:-1]+u[1:-1,2:])/2
    vs1=(v[1:-2,:-1]+v[2:-1,:-1])/2
    vn1=(v[1:-2,1:]+v[2:-1,1:])/2
        
    G1=(F1C(ue1,uw1,us1,un1,vs1,vn1,dx,dy)+FV(u[1:-1,1:-1],u[2:,1:-1],u[:-2,1:-1],u[1:-1,2:],u[1:-1,:-2],dx,dy,mu))
    ut[1:-1,1:-1]=u[1:-1,1:-1]+(dt/1)*G1

    
    ve12=(v[1:-1,1:-1]+v[2:,1:-1])/2
    vw12=(v[1:-1,1:-1]+v[:-2,1:-1])/2
    vs12=(v[1:-1,1:-1]+v[1:-1,:-2])/2
    vn12=(v[1:-1,1:-1]+v[1:-1,2:])/2
    us12=(u[:-1,1:-2]+u[:-1,2:-1])/2
    un12=(u[1:,1:-2]+u[1:,2:-1])/2
        
    G2=(F2C(ve12,vw12,vs12,vn12,us12,un12,dx,dy)+FV(v[1:-1,1:-1],v[2:,1:-1],v[:-2,1:-1],\
                             v[1:-1,2:],v[1:-1,:-2],dx,dy,mu))
    vt[1:-1,1:-1]=v[1:-1,1:-1]+(dt/1)*G2    
    
    #for i in range(len(bu)):
    #    ut[bu[i,0]][bu[i,1]]=0
    #
    #for i in range(len(bv)):
    #    vt[bv[i,0]][bv[i,1]]=0
        
    #ut[:,0]=2*U-ut[:,1]
    #ut[:,-1]=2*U-ut[:,-2]
    #ut[1,1:-1]=U
    #ut[-1,1:-1]=ut[-1,1:-1]-U*(ut[-1,1:-1]-ut[-2,1:-1])*(dt/dx)
    #
    #
    #vt[0,:]=0-vt[1,:]
    #vt[-1,:]=0-vt[-2,:]
    #vt[1:-1,1]=0
    #vt[1:-1,-1]=0
    
    ut[:,0]=2*0-ut[:,1]
    ut[:,-1]=2*U-ut[:,-2]
    
    
    vt[0,:]=0-vt[1,:]
    vt[-1,:]=0-vt[-2,:]

    
    for it in range(maxit):
        for i in range(1,Nx):
            for j in range(1,Ny):
                p[i][j]=w*0.25*(p[i][j+1]+p[i][j-1]+p[i+1][j]+p[i-1][j]-(1*dy/(1*dt))*(vt[i][j]-vt[i][j-1])-\
                       (1*dx/(1*dt))*(ut[i][j]-ut[i-1][j]))+(1-w)*p[i][j]    
        
        p[:,0]=p[:,1]
        p[:,-1]=p[:,-2]

        p[0,:]=p[1,:]
        p[-1,:]=p[-2,:]

    u[1:-1,1:-1]=ut[1:-1,1:-1]-(dt/(dx))*(p[2:-1,1:-1]-p[1:-2,1:-1])

    v[1:-1,1:-1]=vt[1:-1,1:-1]-(dt/(dy))*(p[1:-1,2:-1]-p[1:-1,1:-2])
    
    #u[:,0]=2*U-u[:,1]
    #u[:,-1]=2*U-u[:,-2]
    #u[1,1:-1]=U
    #u[-1,1:-1]=u[-1,1:-1]-U*(u[-1,1:-1]-u[-2,1:-1])*(dt/dx)
    #
    #
    #v[0,:]=0-vt[1,:]
    #v[-1,:]=0-vt[-2,:]
    #v[1:-1,1]=0
    #v[1:-1,-1]=0
    
    u[:,0]=2*0-u[:,1]
    u[:,-1]=2*U-u[:,-2]
    
    
    v[0,:]=0-v[1,:]
    v[-1,:]=0-v[-2,:]
    


uu=(u[:,:-1]+u[:,1:])*0.5
vv=(v[:-1,:]+v[1:,:])*0.5

uu=uu.T
vv=vv.T

plt.figure()
plt.contourf(X,Y,np.sqrt(uu**2+vv**2))
#plt.fill(xcircle,ycircle,'k')
plt.axis('equal')
plt.show()
