import matplotlib.pylab as pl
import numpy as np
from  pylab import *
from mpl_toolkits.mplot3d import  Axes3D
pl.style.use('dark_background')
L=1 
#properties of wood
#k=0.274
#c=2268
#ro=450
#Properties of aluminum bar
      
k=205
c=880
ro=2698.4

Kapa=k/(c*ro)

#initial and boundary conditions
Tinic=20
Tfronte=10


print("\t\t\t NUMERICAL SOLUTION ")
#Creation of deltas x
n=int(input("\nEnter the number of segments of x:"))
Δx=1/(n-1)
x=np.linspace(0,1,n)

#Von Neumann-Courant condition
print(f'\nThe von Neumann-Courant condition requires a Δt less than {((Δx)**2)/(2*Kapa)}')
Δt=float(input("Enter your value of Δt:"))
eta=(Kapa*Δt)/((Δx)**2)
nt=int(input(f'\nEnter the number of steps in time:'))

t=np.arange(0,nt,1)*Δt
X,Ti=np.meshgrid(x,t)

Tncomp=np.zeros((nt,n))#Array to compare analytical and numerical solution
Tacomp=np.zeros((nt,n))#Array to compare analytical and numerical solution




fig = plt.figure()
ax = fig.add_subplot(projection='3d')
def temperatura(x,t):#make the numeriacl solution 
   
    T=np.ones(n)*Tinic#initial conditions
    T[0]=Tfronte#boundary conditions
    T[n-1]=Tfronte

    Tauxiliar=np.zeros(n)
    T_x_t=np.zeros((nt,n))

    for j in range(nt):
        for i in range(n):
            if i==0 or i==n-1:
                Tauxiliar[i]=Tfronte
                T_x_t[j][i]=Tfronte
            else:
                Tauxiliar[i]=T[i]+eta*(T[i-1]+T[i+1]-2*T[i])
                T_x_t[j][i]=T[i]+eta*(T[i-1]+T[i+1]-2*T[i])

        for i in range(n):
            T[i]=Tauxiliar[i]

    for j in range(nt):#copy the values to compare
        for i in range(n):
            Tncomp[j][i]=T_x_t[j][i]
    return(T_x_t)
ax.contour(X,Ti,temperatura(X,Ti),colors='black')    
ax.plot_surface(X,Ti,temperatura(X,Ti),alpha=0.8,cmap='jet')
pl.title('Numerical Solution and Isotherms')
ax.set_xlabel('Length (m)')
ax.set_ylabel('Tine (s)')
ax.set_zlabel('Temperature (°C)')
pl.show()


print("\n\t\t\tANALYTICAL SOLUTION")

#This function calculates the optimal number of terms to approximate the analytical solution
#but never exceed 400 terms
#due to the complexity of the algorithm I put it as a comment because it requires a lot of computing time
'''nterminos=0.0      
def comparacion(x,t):
    cont=[]

    for i in range(1,n):
        for  j in range(nt):

            term=0
            suma=0
            k=1
            contador=0
            eps=10**(-8)
            var=True
            while var==True:
                term=((4*Tinic)/(k*pi))*sin(k*pi*x[i])*exp(-(k**2)*(pi**2)*Kapa*t[j])
                suma+=term
                k+=2
                contador+=1
                comp=abs(term/suma)
                if comp<eps:
                    var=False  

            cont.append(contador)
    
    for i in range(len(cont)):
        cont[i]=cont[i]**2

    suma=0
    for i in range(len(cont)):
        suma+=cont[i]

    suma=suma/len(cont)
    nterminos=int(sqrt(suma))    
    print(f'\nIt is recommended to take {nterminos} terms of the analytical solution')
comparacion(x,t)'''




fig = plt.figure()
ax = fig.add_subplot(projection='3d')
def Graficateorica(x,t):
    z=0
    p=400#int(input("How many terms do you want to take"))
    for i in range(1,p*2):#Take 400 terms of the analytical solution calculated in the previous function
        if i%2==0:
            pass
        else:
            z+=((4*Tinic)/(i*np.pi))*np.sin(i*np.pi*x)*np.exp(-(i**2)*(np.pi**2)*Kapa*t)

    for j in range(nt):#copy the values for later comparison
        for i in range(n):
            Tacomp[j][i]=z[j][i]

    return z
ax.plot_surface(X,Ti,Graficateorica(X,Ti),alpha=0.8,cmap='jet')
pl.title('Analytical solution')
ax.set_xlabel('Length (m)')
ax.set_ylabel('Time (s)')
ax.set_zlabel('Temperature (°C)')
pl.show()





def compara(Tacomp,Tncomp):#compare numerical and analytical solutions at each point of the grid
    Lista=[]
    suma=0
    for j in range(nt):
        for i in range(n):
            if Tacomp[j][i]==0:
                error=abs(Tacomp[j][i]-Tncomp[j][i])
                Lista.append(error)
            else:
                error=abs(Tacomp[j][i]-Tncomp[j][i])
                error=error/Tacomp[j][i]
                Lista.append(error)
    
    for i in range(len(Lista)):
        suma=Lista[i]+suma 
    
    promedio=(suma/len(Lista))*100
    print(f'percentage error\nE={promedio}%')
compara(Tacomp,Tncomp)
