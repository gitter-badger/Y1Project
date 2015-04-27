import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

# Features of CMS detector
B = 3.8 # Magnetic field strength, units: Tesla
r_sol = 2.950 # Radius of solenoid volume, units: meters
z_sol = 3.00 # Length of solenoid volume, units: meters

# initial particle momentum
pz = 1. # units GeV/c
pt = 20. # units: GeV/c

# initial particle position
x0 = 0. # units: meters
y0 = 0. # units: meters
z0 = 0. # units: meters

# initial angle in x-y plane
phi0 = 0.

# Create 2d and 3d figures and axes
# Draw CMS detector (outline of inner surface of solenoid) in 2d and 3d
fig3 = plt.figure(1)
ax3 = fig3.add_subplot(111, projection='3d')
fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
x=np.linspace(-r_sol, r_sol, 100)
z=np.linspace(-z_sol, z_sol, 100)
Xc, Zc=np.meshgrid(x, z)
Yc = np.sqrt(r_sol**2-Xc**2)
y = np.sqrt(r_sol**2-x**2)
ax3.plot_surface(Xc, Yc, Zc,  rstride=4, cstride=4, color='b', alpha=0.2)
ax3.plot_surface(Xc, -Yc, Zc,  rstride=4, cstride=4, color='b', alpha=0.2)
ax3.set_xlabel("X [m]")
ax3.set_ylabel("Y [m]")
ax3.set_zlabel("Z [m]")
ax3.set_xlim3d(-3.2,3.2)
ax3.set_ylim3d(-3.2,3.2)
ax3.set_zlim3d(-3.2,3.2)
ax2.set_xlabel("X [m]")
ax2.set_ylabel("Y [m]")
ax2.set_xlim(-3.2,3.2)
ax2.set_ylim(-3.2,3.2)
ax2.plot(x,y,color='b',label='CMS solenoid')
ax2.plot(x,-y,color='b')

# Derivactions of motion in magnetic field and helix parameterization
# http://www.physics.iitm.ac.in/~sercehep2013/track2_Gagan_Mohanty.pdf

# Calculate radius of curvature
Rc = pt / (0.3*B) # units: meters

# calculate dip angle
ldip = np.arctan(pz/pt)

# Create parameters of helix
s = np.linspace(0, 0 + 1 * np.pi, 1000)
z = s*np.sin(ldip) + z0
x = x0 + Rc*(np.cos(phi0+s*np.cos(ldip)/Rc) - np.cos(phi0))
y = y0 + Rc*(np.sin(phi0+s*np.cos(ldip)/Rc) - np.sin(phi0))

# don't plot helix beyond tracker volume
r = np.sqrt(x*x+y*y)
for i in range(len(r)):
  if r[i] > r_sol or abs(z[i]) > z_sol:
    print "Truncating at %ith point which has (r,z)=(%f,%f) (x,y)=(%f,%f) z/r=%f pz/pt=%f Rc=%f" % (i,r[i],z[i],x[i],y[i],z[i]/r[i],pz/pt,Rc)
    x=x[:i]
    y=y[:i]
    z=z[:i]
    break

# Plot the helix
ax3.plot(x,y,z, label='Particle path', color='r')
ax2.plot(x,y,label='Particle path',color='r')
ax2.legend()

# Show the figures we've made
plt.show()

