import numpy as np
import sys
###
###INPUT DATA
###

sidelength=0.254  #size of the RVE side [m]
nel=8  #number of elements per side
spacingY=0.127 #spacing of horizontal rebars (in y direction) [m]
spacingX=0.1524 #spacing of vertical rebars in (in x direction) [m]

import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
geomObj_1 = geompy.MakeMarker(0, 0, 0, 1, 0, 0, 0, 1, 0)
sk = geompy.Sketcher2D()
sk.addPoint(-sidelength/2, -sidelength/2)
sk.addSegmentAbsolute(0.000000, -sidelength/2)
sk.addSegmentAbsolute(sidelength/2, -sidelength/2)
sk.addSegmentAbsolute(sidelength/2, 0.000000)
sk.addSegmentAbsolute(sidelength/2, sidelength/2)
sk.addSegmentAbsolute(0.000000, sidelength/2)
sk.addSegmentAbsolute(-sidelength/2, sidelength/2)
sk.addSegmentAbsolute(-sidelength/2, 0.000000)
sk.close()
Sketch_1 = sk.wire(geomObj_1)
Face_1 = geompy.MakeFaceWires([Sketch_1], 1)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Sketch_1, 'Sketch_1' )
geompy.addToStudy( Face_1, 'Face_1' )


###
### SMESH component
###

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
Nb_Segments_1 = smesh.CreateHypothesis('NumberOfSegments')
Nb_Segments_1.SetNumberOfSegments( int(nel/2) )
Regular_1D = smesh.CreateHypothesis('Regular_1D')
Quadrangle_2D = smesh.CreateHypothesis('Quadrangle_2D')
Mesh_1 = smesh.Mesh(Face_1)
status = Mesh_1.AddHypothesis(Nb_Segments_1)
status = Mesh_1.AddHypothesis(Regular_1D)
status = Mesh_1.AddHypothesis(Quadrangle_2D)
isDone = Mesh_1.Compute()

#Create group of all faces / boundary elements
all2dElem=Mesh_1.CreateEmptyGroup(SMESH.FACE,"all2dElem")
all2dElem.AddFrom(Mesh_1.mesh)
conBoundSet=Mesh_1.CreateEmptyGroup(SMESH.EDGE,"conboundset")
conBoundSet.Add(Mesh_1.GetElementsByType(SMESH.EDGE))


#Compute the preliminary locations of reinforcement nodes
#and find closest concrete nodes
reSize=sidelength/nel
#horizontal reinforcement
if ( spacingY >= sidelength and spacingY <= 5*sidelength): 
    #only one rebar fits - put it in the centre
    nrex=1
    rexNodes=np.zeros((nel+1,2))
    for i in range(nel+1):
        rexNodes[i,0]=-sidelength/2 + i*reSize
        rexNodes[i,1]=0.0
elif ( spacingY < sidelength and spacingY > 0 ):
    #more than one rebar fit within the RVE - put them symetrically
    nrex=int(sidelength * (1/spacingY) + 1e-3 )
    rexNodes=np.zeros((nel+1,2*nrex))
    #calculate node coordinates (2 columns per rebar)
    for i in range(nrex):
        for j in range(nel+1):
            rexNodes[j,2*(i+1)-2]=-sidelength/2 + j*reSize
            rexNodes[j,2*(i+1)-1]=-(nrex-1) * spacingY/2 + i*spacingY
elif ( spacingY == 0 ):
    nrex=0

#vertical reinforcement
if ( spacingX >= sidelength and spacingX <= 5*sidelength):
    #only one rebar fits - put it in the centre
    nrey=1
    reyNodes=np.zeros((nel+1,2))
    for i in range(nel+1):
        reyNodes[i,0]=0.0
        reyNodes[i,1]=-sidelength/2 + i*reSize
elif ( spacingX < sidelength and spacingX > 0 ):
    #more than one rebar fit within the RVE - put them symetrically
    nrey=int(sidelength * (1/spacingX) + 1e-3)
    reyNodes=np.zeros((nel+1,2*nrey))
    #calculate node coordinates (2 columns per rebar)
    for i in range(nrey):
        for j in range(nel+1):
            reyNodes[j, 2*(i+1)-2]=-(nrey-1) * spacingX/2 + i*spacingX
            reyNodes[j, 2*(i+1)-1]=-sidelength/2 + j*reSize
elif ( spacingX == 0 ):
    nrey=0

#Find closest concrete nodes
conRexNodeNb=[]
conReyNodeNb=[]
for j in range(nrex):
    templist=[]
    
    for i in range(nel+1):
        nodenum=Mesh_1.FindNodeClosestTo(rexNodes[i,2*j],rexNodes[i,2*j+1],0.0)
        templist.append(nodenum)
    
    conRexNodeNb.append(templist)

for j in range(nrey):
    templist=[]
    
    for i in range(nel+1):
        nodenum=Mesh_1.FindNodeClosestTo(reyNodes[i,2*j],reyNodes[i,2*j+1],0.0)
        templist.append(nodenum)
    
    conReyNodeNb.append(templist)

#Duplicate nodes and create reinforcement elements
rexNodeNb=[]
reyNodeNb=[]
for j in range(nrex):
    templist=[]
    
    for i in range(nel+1):
        nodenum=Mesh_1.AddNode(rexNodes[i,2*j],rexNodes[i,2*j+1],0.0)
        templist.append(nodenum)
    
    rexNodeNb.append(templist)

for j in range(nrey):
    templist=[]
    
    for i in range(nel+1):
        nodenum=Mesh_1.AddNode(reyNodes[i,2*j],reyNodes[i,2*j+1],0.0)
        templist.append(nodenum)
    
    reyNodeNb.append(templist)

rexElNb=[]
reyElNb=[]
for j in range(nrex):
    templist=[]
    
    for i in range(nel):
        elnum=Mesh_1.AddEdge([rexNodeNb[j][i], rexNodeNb[j][i+1]])
        templist.append(elnum)
    
    rexElNb.append(templist)

for j in range(nrey):
    templist=[]
    
    for i in range(nel):
        elnum=Mesh_1.AddEdge([reyNodeNb[j][i], reyNodeNb[j][i+1]])
        templist.append(elnum)
    
    reyElNb.append(templist)


#Create reinforcement groups 
reinfX=Mesh_1.CreateEmptyGroup(SMESH.EDGE,"reinfX")
for j in range(nrex):
    reinfX.Add(rexElNb[j])

reinfY=Mesh_1.CreateEmptyGroup(SMESH.EDGE,"reinfY")
for j in range(nrey):
    reinfY.Add(reyElNb[j])

reinfXbound=Mesh_1.CreateEmptyGroup(SMESH.NODE,"reinfXbound")
for j in range(nrex):
    reinfXbound.Add([rexNodeNb[j][0], rexNodeNb[j][-1]])

reinfYbound=Mesh_1.CreateEmptyGroup(SMESH.NODE,"reinfYbound")
for j in range(nrey):
    reinfYbound.Add([reyNodeNb[j][0], reyNodeNb[j][-1]])

#Create interface elements 
interfaceXElements=[]
for j in range(nrex):
    if (len(conRexNodeNb[j]) == len(rexNodeNb[j])):
        
        templist=[]
        for i in range(nel):
            elnum=Mesh_1.AddFace([conRexNodeNb[j][i], conRexNodeNb[j][i+1], rexNodeNb[j][i+1], rexNodeNb[j][i]])
            templist.append(elnum)
        
        interfaceXElements.append(templist)
    else:
        print("Steel/concrete mesh mismatch")

interfaceX=Mesh_1.CreateEmptyGroup(SMESH.FACE,"InterfaceX")
for j in range(nrex):
    interfaceX.Add(interfaceXElements[j])

interfaceYElements=[]
for j in range(nrey):
    if (len(conReyNodeNb[j]) == len(reyNodeNb[j])):
        
        templist=[]
        for i in range(nel):
            elnum=Mesh_1.AddFace([conReyNodeNb[j][i], conReyNodeNb[j][i+1], reyNodeNb[j][i+1], reyNodeNb[j][i]])
            templist.append(elnum)
        
        interfaceYElements.append(templist)
    else:
        print("Steel/concrete mesh mismatch")


interfaceY=Mesh_1.CreateEmptyGroup(SMESH.FACE, "InterfaceY")
for j in range(nrey):
    interfaceY.Add(interfaceYElements[j])


#Creating boundary groups
bcset=Mesh_1.CreateEmptyGroup(SMESH.NODE, "bcset")
bcset.Add(conBoundSet.GetNodeIDs())
bcset.Add(reinfXbound.GetListOfID())
bcset.Add(reinfYbound.GetListOfID())

#Creating groups of weakened elements
weakXEl=[]
for j in range(nrex):
    for i in range(nel):
        foundEl=Mesh_1.FindElementsByPoint(rexNodes[i][2*j]+1e-3, rexNodes[i][2*j+1]-1e-3, 0.0, SMESH.FACE, all2dElem)
        if len(foundEl)==1:
            weakXEl.append(foundEl[0])
        else:
            print("No element found")

weakYEl=[]
for j in range(nrey):
    for i in range(nel):
        foundEl=Mesh_1.FindElementsByPoint(reyNodes[i][2*j]+1e-3, reyNodes[i][2*j+1]+1e-3, 0.0, SMESH.FACE, all2dElem)
        if len(foundEl)==1:
            weakYEl.append(foundEl[0])
        else:
            print("No element found")

weakXYEl=list( set(weakXEl) & set(weakYEl) )

weakX=Mesh_1.CreateEmptyGroup(SMESH.FACE,"weakX")
weakX.Add(weakXEl)
weakY=Mesh_1.CreateEmptyGroup(SMESH.FACE,"weakY")
weakY.Add(weakYEl)
weakXY=Mesh_1.CreateEmptyGroup(SMESH.FACE,"weakXY")
weakXY.Add(weakXYEl)
weakX.Remove(weakXYEl)
weakY.Remove(weakXYEl)

#Export to UNV
path='rvemesh.unv'
Mesh_1.ExportUNV(path)

# sys.exit() 