#!/bin/bash
~/Software/generator/generator.exe generator.in.ctrl 
qdelaunay Qt i < nodes.dat > delaunay.dat 
qvoronoi p Fv < nodes.dat > voronoi.dat 
~/Software/converter/converter.exe control.in.ctrl nodes.dat delaunay.dat voronoi.dat 