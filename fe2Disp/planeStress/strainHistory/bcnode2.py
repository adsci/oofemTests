#   Copyright (c) 2017, Adam Sciegaj, Chalmers University of Technology
#
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import numpy as np
import re
def giveUserDefBC(iCoords, iDofNum, iTime):
    #Read the strain history from the txt file produced by Matlab/Octave
    fil=open('strainHistory.txt')
    inpFile=fil.readlines()
    fil.close

    strainRegex=re.compile(r'(\d+)\s+(-?\d\.\d{6}e.\d{2})\s+(-?\d\.\d{6}e.\d{2})\s+(-?\d\.\d{6}e.\d{2})\n?')

    strainList=[]
    for i in range(len(inpFile)):
        if strainRegex.findall(inpFile[i]) != []:
            time=int(strainRegex.findall(inpFile[i])[0][0])
            exx=float(strainRegex.findall(inpFile[i])[0][1])
            eyy=float(strainRegex.findall(inpFile[i])[0][2])
            gxy=float(strainRegex.findall(inpFile[i])[0][3])
            data=[time, exx, eyy, gxy]
            strainList.append([time, exx, eyy, gxy])
        
    strainHist=np.array(strainList)

    presVal=0.0
    iTime=int(iTime)
    strain = [ [strainHist[iTime-1][1], strainHist[iTime-1][3]/2], [strainHist[iTime-1][3]/2 , strainHist[iTime-1][2] ] ]
    
    if iDofNum == 1:
        presVal = strain[0][0]
    else:
        print('Warning: no rule for dof number: ', iDofNum)
           
    #	print 'presVal: ',presVal
    return presVal


    
