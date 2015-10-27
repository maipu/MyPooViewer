# MyPooViewer
Viewer for .off and some .m3d formats. Convert from .off to .m3d and .m3d to off. Allows move nodes and rotate.
To view requires PyGame !!

usage: viewer.py INPUT [OUTPUT] [-g]

if INPUT is m3d file then OUTPUT will be .off
if INPUT is .off file then the OUTPUT will be m3d
-g is for view the figure of the INPUT


readFile("INPUT"): read a file and return an Element Class.

to view:
  someElement.view()

to move a point:
  someElement.vertices[v].x += 1

to rotate a point:
around the Y axis:
  someElement.vertices[v] = someElement.vertices[v].rotateY(DEGREE,[X,Z])
  where [X,Z] are the coordinates of the Y axis to rotate arround. Default is [0,0].
for X axis:
  same but the axis coords are [Y,Z]
for Z axis:
  same but the axis coords are [X,Y]

to save the moved points:
  someElement.vertices[v].x += 1
  someElement.save()
  someElement.writem3d("file.m3d")


Original Cube Rotating Code:
https://github.com/The-Penultimate-Defenestrator/Python/blob/master/wireframe.py
