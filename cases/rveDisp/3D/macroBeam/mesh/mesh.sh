#!/bin/bash
~/Software/generator/generator.exe generator.in 
qdelaunay Qt i < nodes.dat > delaunay.dat 
qvoronoi p Fv < nodes.dat > voronoi.dat 
~/Software/converter/converter.exe control.in nodes.dat delaunay.dat voronoi.dat 