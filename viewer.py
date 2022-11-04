#HOLAAAAAAAAAAAAAAAAAA

import sys
import math
__main__display = False
if "-g" in sys.argv:
    __main__display = True
    sys.argv.remove("-g")
    import pygame
noPygame = False
if __name__ != "__main__":
    import threading
    try:
        import pygame
    except:
        noPygame = True

# Globales
xrot = 0
yrot = 0

viewing = False
sim = None

class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
    def rotateX(self, angle, axisX=[0,0]):
        # Roatates the point around the X by the given angle in degrees
        rad = -angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        y = self.y * cosa - (self.z-axisX[1]) * sina
        z = (self.y-axisX[0]) * sina + self.z * cosa
        return Point3D(self.x, y, z)
        
    def rotateY(self, angle, axisY=[0,0]):
        # Rotates the point around the Y by the given angle in degrees
        rad = -angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        z = self.z * cosa - (self.x-axisY[0]) * sina
        x = (self.z-axisY[1]) * sina + self.x * cosa
        return Point3D(x, self.y, z)
        
    def rotateZ(self, angle, axisZ=[0,0]):
        # Rotates the point around the Z by the given angle in degrees
        rad = -angle * math.pi / 180
        cosa = math.cos(rad)
        sina = math.sin(rad)
        x = self.x * cosa - (self.y-axisZ[1])* sina 
        y = (self.x-axisZ[0]) * sina + self.y* cosa
        return Point3D(x, y, self.z)
        
    def project(self, win_width, win_height, fov, viewer_distance):
        # Transforms the 3D point into a 2D projection
        fov = fov*2
        viewer_distance = viewer_distance*2
        factor = fov / (viewer_distance - self.z)
        x = self.x * factor + win_width / 2
        y = -self.y * factor + win_height / 2
        return Point3D(x, y, factor*0.1)   #antes Z era 1


class Simulation:
    def __init__(self, win_width=800, win_height=600):
        self.win_width = win_width
        self.win_height = win_height

        self.vertices = []
        self.faces = []
        

    def run(self):
        global noPygame
        if noPygame:
            print "Es necesaria la libreria 'pygame'"
            return
        pygame.init()
        
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        pygame.display.set_caption("MyPooViewer 0.5")
        
        self.clock = pygame.time.Clock()
        
        # Variables de control
        self.active = True
        self.freeze = False
        while self.active:
            while self.freeze:
                pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #print "ADIOOSS"
                    self.active = False
                    #sys.exit()
            self.clock.tick(50)
            self.screen.fill((0,0,0))
            

            # Controls Mouse Position
            global xrot
            global yrot
            yvar, xvar = pygame.mouse.get_rel()
            if pygame.mouse.get_pressed()[0]:
                if abs(xvar) < 4 or abs(yvar) < 4:
                    if abs(xvar) < abs(yvar):
                        xvar = 0
                    else:
                        yvar = 0
                if abs(xvar) < 2:
                    xvar = 0
                if abs(yvar) < 2:
                    yvar = 0
                
                xrot += xvar
                yrot += yvar

            #Will hold the transformed vertices
            t = []
            
            for i in range(0, len(self.vertices)):
                self.vertices[i] = self.vertices[i].rotateX(-xrot / 2).rotateY(-yrot / 2).rotateZ(0)
            xrot, yrot = 0, 0
            for v in self.vertices:
                # Rotate the point around the X axis, then the Y axis, and finally the Z axis
                r = v#v.rotateX(-xrot / 2).rotateY(-yrot / 2).rotateZ(0)
                
                # Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                x, y = int(p.x), int(p.y)

                # Put the point in the list of transformed vertices
                t.append(p)

            for f in self.faces:
                f_=list(f)
                f_.append(f_[0])
                f_=f_[1:]
                for a1,a2 in zip(f,f_):
                    pygame.draw.line(self.screen, (255, 255, 255), (t[a1].x, t[a1].y), (t[a2].x, t[a2].y))
            for v in self.vertices:
                # Draw dots on the edges of the cube
                r = v#v.rotateX(-xrot / 2).rotateY(-yrot / 2).rotateZ(0)
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                x, y = int(p.x), int(p.y)
                radius = int(p.z)
                if v==self.vertices[0]:
                    pygame.draw.circle(self.screen, (255, 0, 0), (x, y), radius)
                else:
                    pygame.draw.circle(self.screen, (0, 255, 255), (x, y), radius)
                #radius += 10
                
            pygame.display.flip()
        
        pygame.quit()


class Element():
    def __init__(self):
        self.vertices = []
        self.faces = []
        
        self._vertices = []
    
    def restore(self):
        self.vertices = list([Point3D(p.x,p.y,p.z) for p in self._vertices])
        global viewing
        global sim
        if viewing:
            sim.freeze = True
            sim.vertices = list(self.vertices)
            sim.faces = list(self.faces)
            sim.freeze = False
    
    def save(self):
        self._vertices = list(self.vertices)
    
    def view(self):
        global viewing
        global sim
        if viewing:
            sim.freeze = True
            sim.vertices = list(self.vertices)
            sim.faces = list(self.faces)
            sim.freeze = False
            return
        sim = Simulation()
        sim.vertices = list(self.vertices)
        sim.faces = list(self.faces)
        t = threading.Thread(target=self.hilo, args = [])
        t.daemon = False
        t.start()
        viewing = True
        
        
    def hilo(*args):
        global viewing
        global sim
        sim.run()
        viewing = False
    
    def writem3d(self, fileName):
        if self.__class__ == Chungungo and self.template == False:
            print "Figura no indexada. No Guardare el archivo y no me obligaras."
            return
        
        if self.__class__ == Chungungo:
            figure2 = figuresType[self.template]()
            figure2._vertices = self._vertices
            figure2.faces = self.faces
            self = figure2
        
        with open(fileName, 'w') as file:
            count = -1
            points = ""
            file.write("[Nodes, ARRAY1<STRING>]\n")
            file.write(str(len(self._vertices))+"\n")
            file.write("\n")
            for p in self._vertices:
                file.write("1 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
                count += 1
                points += str(count) + " "
            file.write("\n")
            file.write("[Elements, ARRAY1<STRING>]\n")
            file.write("1\n")
            file.write("\n")
            letra = ""
            for code, clase in figuresType.items():
                if clase == self.__class__:
                    letra += code+" "
                    break
            file.write(letra + points + "1000.0 0.45 1.0\n")
    
    def writeoff(self, fileName):
        with open(fileName, 'w') as file:
            file.write("OFF\n")
            file.write(str(self.puntos) + " " + str(len(self.faces))+ " " +str(self.aristas)+"\n")
            for p in self._vertices:
                file.write(str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
            for f in self.faces:
                file.write(str(len(f))+ " ")
                for i in range(0,len(f)):
                    file.write(str(f[i]) + " ")
                file.write("\n")


class Hex(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 8
        self.aristas = 12
        self.faces = [(0,1,2,3), (4,5,6,7), (0,1,5,4), (2,3,7,6), (1,2,6,5), (3,0,4,7)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(0,6,0,0)]
        
        

class Tet(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 4
        self.aristas = 6
        self.vertices = []
        self.faces = [(0,1,2),(0,1,3),(1,2,3),(2,0,3)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(3,0,0,0)]

class Pyramid(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 5
        self.aristas = 8
        self.vertices = []
        self.faces = [(0,1,2,3),(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
        self.signature = [self.puntos,self.aristas,len(self.faces), (4,1,0,0)]

class Prism(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 6
        self.aristas = 9
        self.vertices = []
        self.faces = [(0,1,2),(3,4,5),(0,3,5,2),(0,3,4,1),(1,4,5,2)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(2,3,0,0)]

class TetCom(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 7
        self.aristas = 12
        self.vertices = []
        self.faces = [(0,1,2,3),(0,1,5,4),(1,2,5),(2,3,6),(3,0,4,6),(4,5,6),(5,2,6)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(4,3,0,0)]

class DefPrism(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 6
        self.aristas = 11
        self.vertices = []
        self.faces = [(0,1,2,3),(0,4,1),(1,4,2),(2,3,5),(3,5,0),(0,5,4),(4,2,5)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(6,1,0,0)]

class DefTetCom(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 7
        self.aristas = 14
        self.vertices = []
        self.faces = [(0,1,2,3),(0,4,1),(1,4,2),(2,3,5),(3,5,0),(0,6,4),(0,5,6),(2,6,4),(2,5,6)]
        self.signature = [self.puntos,self.aristas,len(self.faces),(8,1,0,0)]

class Chungungo(Element):
    def __init__(self):
        Element.__init__(self)
        self.puntos = 0
        self.aristas = 0
        self.vertices = []
        self.faces = []
        self.signature = [0,0,0,(0,0,0,0)]
        self.template = ""


figuresType = { "H":Hex,
                "T":Tet,
                "P":Pyramid,
                "R":Prism,
                "TC":TetCom,
                "DP":DefPrism,
                "DTC":DefTetCom,
                }

def readFile(fileName):
    fileType = "md3"
    with open(fileName, 'r') as file:
        if file.readline().strip() != "OFF":
            file.readline()
            nodes = []
            file.readline()
            while 1:
                line = file.readline()
                if line.rstrip() == "":
                    break
                x, y , z = line.split()[1:4]
                nodes.append(Point3D(x,y,z))
            while 1:
                line = file.readline()
                if line.rstrip() != "":
                    break
            file.readline()
            file.readline()
            line = file.readline().split()
            figCode = line[0]
            figure = figuresType[figCode]()
            points = line[1:figure.puntos+1]
            for p in points:
                figure.vertices.append(nodes[int(p)])
        else:
            fileType = "off"
            _nodes, _faces, _edges = file.readline().split()
            figure = Chungungo()
            figure.puntos = int(_nodes)
            figure.aristas = int(_edges)
            for i in range(0,figure.puntos):
                x,y,z = file.readline().split()
                figure.vertices.append(Point3D(x,y,z))
            travoltaCage = [0,0,0,0]
            for i in range(0,int(_faces)):
                line = file.readline().split()
                travoltaCage[int(line[0])-3] += 1
                figure.faces.append([int(x) for x in line[1:]])
            figure.signature = [figure.puntos, int(_edges), int(_faces), tuple(travoltaCage)]
            print figure.signature
            control = False
            for s in figuresType.values():
                if s().signature == figure.signature:
                    print s.__name__ + " detectado"
                    if control == True:
                        print "Mas de una figura con la misma 'signature'"
                        print "Revisar D:"
                        break
                    for code, clase in figuresType.items():
                        if clase == s:
                            figure.template = code
                            break
                    control = True
    figure._vertices = list([Point3D(p.x,p.y,p.z) for p in figure.vertices])
    return figure

    
### Descomentar en caso de que fallen las funciones para guardar de la clase Element
""" 
def writem3d(figure,fileName):
    if figure.__class__ == Chungungo and figure.template == False:
        print "Figura no indexada. No Guardare el archivo y no me obligaras."
        return
    
    if figure.__class__ == Chungungo:
        figure2 = figuresType[figure.template]()
        figure2.vertices = figure.vertices
        figure2.faces = figure.faces
        figure = figure2
    
    with open(fileName, 'w') as file:
        count = -1
        points = ""
        file.write("[Nodes, ARRAY1<STRING>]\n")
        file.write(str(len(figure.vertices))+"\n")
        file.write("\n")
        for p in figure.vertices:
            file.write("1 "+str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
            count += 1
            points += str(count) + " "
        file.write("\n")
        file.write("[Elements, ARRAY1<STRING>]\n")
        file.write("1\n")
        file.write("\n")
        letra = ""
        for code, clase in figuresType.items():
            if clase == figure.__class__:
                letra += code+" "
                break
        file.write(letra + points + "1000.0 0.45 1.0\n")


def writeoff(figure, fileName):
    with open(fileName, 'w') as file:
        file.write("OFF\n")
        file.write(str(figure.puntos) + " " + str(len(figure.faces))+ " " +str(figure.aristas)+"\n")
        for p in figure.vertices:
            file.write(str(p.x)+" "+str(p.y)+" "+str(p.z)+"\n")
        for f in figure.faces:
            file.write(str(len(f))+ " ")
            for i in range(0,len(f)):
                file.write(str(f[i]) + " ")
            file.write("\n")
        
"""

if __name__ == "__main__":
    fileName = sys.argv[1]
    figure = readFile(fileName)
    if len(sys.argv) == 3:  ## viewer.py
        if figure.__class__ != Chungungo:   #si el archivo de origen no es OFF
            figure.writeoff(sys.argv[2])
        else:
            if figure.template != "":
                figure.writem3d(sys.argv[2])
            else:
                print "La figura no se pudo escribir como m3d."
    if __main__display:
        simu = Simulation()
        simu.vertices = list(figure.vertices)
        simu.faces = list(figure.faces)
        simu.run()
