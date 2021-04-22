#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script creating an RVE input file (OOFEM format)
Input parameters:
###GEOMETRY
sidelength  #size of the RVE side [m]
nel  #number of elements per side
spacingY #spacing of horizontal rebars (in y direction) [m]
spacingX #spacing of vertical rebars in (in x direction) [m]
phi_x #diameter of rebars in x direction [m]
phi_y #diameter of rebars in y direction [m]
thick #thickness of the RVE [m]

###MATERIAL MODELS
###CONCRETE - MazarsModel / Concrete3
E_c #Young's modulus [Pa]
nu_c #Poisson's ratio [-]
f_t #tensile strength [Pa]
f_c #compressive strength [Pa]
G_F #fracture energy mode I [N/m]
ac #Mazars parameter
bc #Mazars parameter
#STEEL - MisesMat
E_s #Young's modulus [Pa]
nu_s #Poissons ratio [-]
sig0_x #yield strength (horizontal reinforcement) [Pa]
sig_ux #ultimate strength (horizontal reinforcement )[Pa]
sig0_y #yield strength (vertical reinforcement) [Pa]
sig_uy #ultimate strength (vertical reinforcement )[Pa]

#INTERFACE - BondCEB
s3x #characteristic slip value [m]
s3y #characteristic slip value [m]

@author: adsci
"""

import numpy as np
import sys, os, math
###
###INPUT DATA
###

##GEOMETRY
sidelength=0.254  #size of the RVE side [m]
nel=8  #number of elements per side
spacingY=0.127 #spacing of horizontal rebars (in y direction) [m]
spacingX=0.1524 #spacing of vertical rebars in (in x direction) [m]
nox=3 #number of bars in one horizontal layer [-]
noy=2 #number of bars in one vertical layer [-]
phi_x=0.025 #diameter of rebars in x direction [m]
phi_y=0.010 #diameter of rebars in y direction [m]
thick=0.305 #thickness of the RVE [m]

###MATERIAL MODELS
###CONCRETE - MazarsModel / Concrete3
nu_c=0.2 #Poisson's ratio [-]
f_t=3.7e6 #tensile strength [Pa]
f_c=33e6 #compressive strength [Pa]
ac=2.4 #Mazars parameter
bc=800 #Mazars parameter
#STEEL - MisesMat
sig0_x=420e6 #yield strength (horizontal reinforcement) [Pa]
sig_ux=700e6 #ultimate strength (horizontal reinforcement) [Pa]
sig0_y=450e6 #yield strength (vertical reinforcement) [Pa]
sig_uy=720e6 #ultimate strength (vertical reinforcement) [Pa]

#INTERFACE - BondCEB
s3x=0.010 #characteristic slip value [m]
s3y=0.005 #characteristic slip value [m]


########DEPENDENT PARAMETERS
###GEOMETRY
h_c=sidelength/nel #characteristic element size 
if (spacingX > sidelength):
    scaleX= sidelength / spacingX
elif ( spacingX < sidelength and spacingX > sidelength/2 ):
    scaleX = sidelength / spacingX
else:
    scaleX = 1.0
    
if (spacingY > sidelength):
    scaleY = sidelength / spacingY
elif ( spacingY < sidelength and spacingY > sidelength/2 ):
    scaleY = sidelength / spacingY
else:
    scaleY = 1.0

###MATERIAL MODELS
###CONCRETE - MazarsModel
E_c=21.5e9 * 1 * (f_c/1e7)**(0.333) #Young's modulus [Pa]
G_F=73 * (f_c/1e6)**(0.18) #fracture energy mode I [N/m]
e_0= f_t / E_c #peak strain in tension
ef= e_0 * (G_F * E_c / (h_c * f_t**2) - 0.5) #compressive damage law adjustment factor 
#STEEL - MisesMat
E_s=2e11 #Young's modulus [Pa]
nu_s=0.3 #Poissons ratio [-]
eps_u=0.05 #strain at max force - CARES guide
Hx=(sig_ux - sig0_x) / (eps_u - sig_ux/E_s) #hardening modulus (horizontal reinforcement) [Pa]
Hy=(sig_uy - sig0_y) / (eps_u - sig_uy/E_s) #hardening modulus [Pa]
#INTERFACE - BondCEB
s1=0.001 #Characteristic slip value [m]
s2=0.002 #Characteristic slip value [m]
taumax=2.5 * (f_c/1e6)**0.5  * 1e6 #maximum bond stress [Pa]
tauf=0.4 * taumax #residual bond stress at reinforcement pull-out [Pa]
ks=taumax * (0.1**0.4) / (0.1*s1) #approximation of interface tangential stiffness [Pa]
kn=ks*100 #approximation of interface normal stiffness [Pa]


########WRITE CONTROL FILE
print("***************Writing .ctrl file***************")
try:
    ctrlFile=[]
    ctrlFile.append("rvedd.out\n")
    ctrlFile.append("Reinforced concrete RVE - Dirichlet-Dirichelt BCs\n")
    ctrlFile.append("StaticStructural nsteps 1 deltat 1.0 constrainednrminiter 5 rtolf 1.0e-3 MaxIter 100 minIter 1 stiffmode 2 initialguess 1 nmodules 0 suppress_output\n")
    ctrlFile.append("#vtkxml tstep_all domain_all vars 5 1 4 5 12 52 ipvars 6 1 4 5 12 52 90 stype 1 regionsets 1 1\n")
    ctrlFile.append("#vtkxml tstep_all domain_all vars 1 12 ipvars 3 7 8 81 stype 1 regionsets 2 9 10\n")
    ctrlFile.append("#vtkxml tstep_all domain_all vars 2 98 99 stype 0 regionsets 2 11 12\n")
    ctrlFile.append("domain 2dplanestress\n")
    ctrlFile.append("OutputManager\n")
    ctrlFile.append("ncrosssect 8 nmat 5 nbc 1 nic 0 nltf 1 nset 12\n")
    ctrlFile.append("SimpleCS 1 thick {:.10e} material 1 set 1\n".format(thick))
    ctrlFile.append("SimpleCS 2 thick {:.10e} material 1 set 2\n".format(thick - (noy * math.pi* phi_y**2)/(4*h_c)))
    ctrlFile.append("SimpleCS 3 thick {:.10e} material 1 set 3\n".format(thick - (nox * math.pi* phi_x**2)/(4*h_c)))
    ctrlFile.append("SimpleCS 4 thick {:.10e} material 1 set 4\n".format(thick - math.pi/(4*h_c) * (nox*phi_x**2 + noy*phi_y**2)))
    ctrlFile.append("SimpleCS 5 area {:.10e} material 2 set 9\n".format( noy * math.pi*phi_y**2 / 4  * scaleX ))
    ctrlFile.append("SimpleCS 6 area {:.10e} material 3 set 10\n".format( nox * math.pi*phi_x**2 / 4 * scaleY ))
    ctrlFile.append("InterfaceCS 7 thickness {:.10e} material 4 set 11\n".format( nox * math.pi * phi_x))
    ctrlFile.append("InterfaceCS 8 thickness {:.10e} material 5 set 12\n".format( noy * math.pi * phi_y))
    ctrlFile.append("#MazarsModel 1 d 1.0 E {:.3e} n {} version 1 e0 {:.10e} ac {} bc {} ef {:.10e} tAlpha 1.0 maxOmega 0.9999\n".format(E_c, nu_c, e_0, ac, bc, ef))
    ctrlFile.append("Concrete3 1 d 1.0 E {:.3e} n {} Gf {:.2f} Ft {:.3e} exp_soft 0 tAlpha 1.0\n".format(E_c, nu_c, G_F, f_t))
    ctrlFile.append("MisesMat 2 d 1.0 E {:.3e} n {} sig0 {:.2e} H {:.10e} omega_crit 0 a 0 tAlpha 1.0\n".format(E_s, nu_s, sig0_y, Hy))
    ctrlFile.append("MisesMat 3 d 1.0 E {:.3e} n {} sig0 {:.2e} H {:.10e} omega_crit 0 a 0 tAlpha 1.0\n".format(E_s, nu_s, sig0_x, Hx))
    ctrlFile.append("bondceb 4 kn {:.2e} ks {:.10e} s1 {} s2 {} s3 {} taumax {:.10e} tauf {:.10e}\n".format(kn, ks, s1, s2, s3x, taumax, tauf))
    ctrlFile.append("bondceb 5 kn {:.2e} ks {:.10e} s1 {} s2 {} s3 {} taumax {:.10e} tauf {:.10e}\n".format(kn, ks, s1, s2, s3y, taumax, tauf))
    ctrlFile.append("PrescribedDispSlipBCDirichletRC 1 loadTimeFunction 1 dofs 3 1 2 6 ccoord 3 0.0 0.0 0.0 dispGrad 2 2 {0 0; 0 0} set 5 conboundset 6\n")
    ctrlFile.append("ConstantFunction 1 f(t) 1.0\n")
    ctrlFile.append("set 1 elements\n")
    ctrlFile.append("set 2 elements\n")
    ctrlFile.append("set 3 elements\n")
    ctrlFile.append("set 4 elements\n")
    ctrlFile.append("set 5 nodes\n")
    ctrlFile.append("set 6 elementboundaries\n")
    ctrlFile.append("set 7 nodes\n")
    ctrlFile.append("set 8 nodes\n")
    ctrlFile.append("set 9 elements\n")
    ctrlFile.append("set 10 elements\n")
    ctrlFile.append("set 11 elements\n")
    ctrlFile.append("set 12 elements\n")
    ctrlFile.append("\n")
    ctrlFile.append("group all2dElem\n")
    ctrlFile.append("elemprop set 1\n")
    ctrlFile.append("etype[44] PlaneStress2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group weakY\n")
    ctrlFile.append("elemprop set 2\n")
    ctrlFile.append("etype[44] PlaneStress2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group weakX\n")
    ctrlFile.append("elemprop set 3\n")
    ctrlFile.append("etype[44] PlaneStress2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group weakXY\n")
    ctrlFile.append("elemprop set 4\n")
    ctrlFile.append("etype[44] PlaneStress2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group bcset\n")
    ctrlFile.append("nodeprop set 5\n")
    ctrlFile.append("\n")
    ctrlFile.append("group conboundset\n")
    ctrlFile.append("elemprop set 6\n")
    ctrlFile.append("etype[11]\n")
    ctrlFile.append("\n")
    ctrlFile.append("group reinfYbound\n")
    ctrlFile.append("nodeprop set 7\n")
    ctrlFile.append("\n")
    ctrlFile.append("group reinfXbound\n")
    ctrlFile.append("nodeprop set 8\n")
    ctrlFile.append("\n")
    ctrlFile.append("group reinfY\n")
    ctrlFile.append("elemprop set 9 \n")
    ctrlFile.append("elemprop cs 1\n")
    ctrlFile.append("etype[11] Truss2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group reinfX\n")
    ctrlFile.append("elemprop set 10 \n")
    ctrlFile.append("elemprop cs 1\n")
    ctrlFile.append("etype[11] Truss2d\n")
    ctrlFile.append("\n")
    ctrlFile.append("group InterfaceX\n")
    ctrlFile.append("elemprop set 11 \n")
    ctrlFile.append("etype[44] IntElLine1\n")
    ctrlFile.append("\n")
    ctrlFile.append("group InterfaceY\n")
    ctrlFile.append("elemprop set 12 \n")
    ctrlFile.append("etype[44] IntElLine1\n")
    
    newFilePath='rvedd.ctrl'
    newFile=open(newFilePath,'w')
    for line in ctrlFile:
        newFile.write(line)
    
    newFile.close()
    print("Writing .ctrl file successful")
except:
    print("Writing .ctrl file failed")