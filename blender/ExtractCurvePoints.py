"""
Script to extract the points of a bezier curve and generate the related javascript code for BabylonJS
Coordinate conversion is verified.
How to use?
So far, open the scripting mode, paste the code in the text window and execute. It applies only on the first curve found.
"""

import bpy

import mathutils
from mathutils import *

spline = bpy.data.curves[0].splines[0]

bezierPoints = [];

if len(spline.bezier_points) >= 2:
    r = spline.resolution_u + 1
    segments = len(spline.bezier_points)
    if not spline.use_cyclic_u:
        segments -= 1

    points = []
    for i in range(segments):
        bp={}
        inext = (i + 1) % len(spline.bezier_points)

        knot1 = spline.bezier_points[i].co
        handle1 = spline.bezier_points[i].handle_right
        handle2 = spline.bezier_points[inext].handle_left
        knot2 = spline.bezier_points[inext].co
        bp['k1']=knot1
        bp['k2']=knot2
        bp['h1']=handle1
        bp['h2']=handle2
        bezierPoints.append( bp )

        _points = mathutils.geometry.interpolate_bezier(knot1, handle1, handle2, knot2, r)
        points.extend(_points)

i=0    
for pts in bezierPoints:
    if(i==0):
        print("let curve = BABYLON.Curve3.CreateCubicBezier(")
        print("    v3({}, {}, {}),".format(-pts['k1'].x,pts['k1'].z,-pts['k1'].y))
        print("    v3({}, {}, {}),".format(-pts['h1'].x,pts['h1'].z,-pts['h1'].y))
        print("    v3({}, {}, {}),".format(-pts['h2'].x,pts['h2'].z,-pts['h2'].y))
        print("    v3({}, {}, {}),".format(-pts['k2'].x,pts['k2'].z,-pts['k2'].y))
        print("    20\n);")
    else:
        print("curve = curve.continue(")
        print("    BABYLON.Curve3.CreateCubicBezier(")
        print("    v3({}, {}, {}),".format(-pts['k1'].x,pts['k1'].z,-pts['k1'].y))
        print("    v3({}, {}, {}),".format(-pts['h1'].x,pts['h1'].z,-pts['h1'].y))
        print("    v3({}, {}, {}),".format(-pts['h2'].x,pts['h2'].z,-pts['h2'].y))
        print("    v3({}, {}, {}),".format(-pts['k2'].x,pts['k2'].z,-pts['k2'].y))
        print("        20\n    )\n);")
    i=i+1
    
