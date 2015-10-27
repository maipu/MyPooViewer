from viewer import *
import time
figure = readFile("cube.m3d")

figure.view()


for i in range(0,100):
    figure.vertices[0].x += 0.05
    ## Si se quieren hacer varios archivos, no es necesario visualizar,
    ## pero resulta didactico verlo.
    figure.view()
    figure.save()
    figure.writem3d("cubeTest"+str(i)+".m3d")
    
    ## El sleep es solo para que se visualice cada cambio chico,
    ## de lo contrario solo se ve el nodo en la posicion final.
    time.sleep(0.01)

# Guarda como archivo .off
figure.writeoff("cube.off")

# Restaura a la configuracion inicial de la figura (cubo)
figure.restore()
figure.writem3d("cubeRestored.m3d")


