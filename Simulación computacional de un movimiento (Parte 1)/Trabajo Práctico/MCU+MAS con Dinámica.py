###############################
# Movimiento de una partícula #
###############################

import simplegui
from math import *

########################################
# Inicialización de variables globales #
########################################

# Usamos los valores de la simulación 1.

# Tamaño de la ventana en la que vamos a graficar (en pixels)
WIDTH = 800.
HEIGHT = 800.

# Valores máximos y mínimos de x e y que se graficarán (misma escala en ambos ejes)
xmin = -50
xmax = 50
ymin = -50
ymax = ymin + (xmax-xmin)*HEIGHT/WIDTH

# Radio del círculo con que vamos a representar a nuestra partícula (pixels)
radio=10

# Valor inicial de tiempo
time = 0.

# Paso o incremento temporal
dt = 0.01

# Variables cinemáticas y sus valores iniciales.
pos0x = 0.
posx = pos0x
pos0y = 20.
posy = pos0y
vel0x = 10
velx = vel0x
vel0y = 0
vely = vel0y
ax = 0
ay = 0

#Variables del resorte
l0 = 10
k = 1.25

# Trayectoria
traj=[]
traj.append((posx,posy))

# Características del sistema e interacciones
masa = 5

#########################################
# A continuación se definen los eventos #
#########################################

# Aquí tenemos lo que se grafica
def draw(canvas): 
    
    # Este es un movimiento que integra un Movimiento Circular Uniforme
    # con un Movimiento Armónico Simple.
    canvas.draw_text("Este es un movimiento (MCU+MAS o una superposición?)", (20, 770), 20, "White")
    
    # Dibuja un segmento que une los dos puntos especificados, 
    # de ancho tres y de color gris. Los usamos como referencia
    # para visualizar el movimiento
    canvas.draw_line((0,HEIGHT/2),(WIDTH,HEIGHT/2),3,"Grey")
    canvas.draw_line((WIDTH/2,0),(WIDTH/2,HEIGHT),3,"Grey")
    
    pixelx = WIDTH/(xmax-xmin)*(posx-xmin)
    pixely = -HEIGHT/(ymax-ymin)*(posy-ymin)+HEIGHT
    
    # Dibuja un círculo en la posición indicada por las 
    # coordenadas de la variable "pos"
    # De color verde, radio= valor de la variable "radio" y 
    # un borde de tamaño 2 y también de color verde.
    # Esta partícula está unida a un objeto fijo de color blanco
    # a través de un resorte, representada por una recta de color
    # verde. 
    canvas.draw_circle((pixelx,pixely),radio, 2,"Green","Green")
    canvas.draw_circle((WIDTH/2,HEIGHT/2),radio, 1,"White","White")
    canvas.draw_line((WIDTH/2,WIDTH/2),(pixelx,pixely),3,"Green")

    # Representa los puntos por los que fue transitando la partícula
    for point in traj:
        canvas.draw_point((WIDTH/(xmax-xmin)*(point[0]-xmin),-HEIGHT/(ymax-ymin)*(point[1]-ymin)+HEIGHT),"Green")
    
# Aqui tenemos las instrucciones que se ejecutan en cada
# paso de la simulación
def tick():
    global time #si uno quiere modificar el valor de una variable global, debe incluir estas líneas.
    global posx
    global velx
    global ax
    global posy
    global vely
    global ay
    global traj
    
    
    time += dt #al valor de tiempo previo le suma "dt"
    
    #Cálculo de la amplitud
    A = sqrt(posx**2+posy**2)-l0
    
    # Cálculo de las componentes de la fuerza neta    
    F = k*A
    Fx = F*(-posx/sqrt(posx**2+posy**2))
    Fy = F*(-posy/sqrt(posx**2+posy**2))
    
    # Cálculo de la aceleración
    ax = Fx/masa
    ay = Fy/masa
    
    # Actualización de la posición (aquí tenemos el cálculo
    # de la nueva posición basado en el valor previo de 
    # posición y en la forma en la que se está moviendo 
    # el objeto)
    posx = posx + velx * dt + 0.5 * ax * dt**2
    posy = posy + vely * dt + 0.5 * ay * dt**2
    
    traj.append((posx,posy))

    # Actualización de la velocidad 
    velx = velx + ax * dt 
    vely = vely + ay * dt
    
    # Esto lo utilizamos para calcular la velocidad angular
    # para luego hacer el gráfico de vel. angular en función
    # del tiempo y así justificar la última sección del tp
    #w= (sqrt(velx**2+vely**2))/(sqrt(posx**2+posy**2))
    #print (w,time)

    # Imprime en pantalla los valores de las variables mencionadas.    
    #print (A, sqrt(posx**2+posy**2),time,posx,posy,velx,vely)

# Aquí tenemos una acción de control para iniciar y frenar
# la simulación (más abajo incluimos un botón)
def click():
    if timer.is_running():
        timer.stop()
    else:
        timer.start()
        
# Aquí tenemos una acción de control para reiniciar la 
# simulación (más abajo incluimos otro botón)
def click2():
    global time
    global posx
    global velx
    global posy
    global vely  
    global traj
    posx = pos0x
    velx = vel0x
    posy = pos0y
    vely= vel0y    
    time = 0
    traj=[]

#############################################
# Aquí tenemos los controles de los eventos #
#############################################

# Crea una ventana donde se realiza la representación gráfica
frame = simplegui.create_frame("Movimiento", WIDTH, HEIGHT)
frame.set_canvas_background('Black')

# Aquí tenemos los que se representan en esa ventana
frame.set_draw_handler(draw)
frame.add_button("START/STOP",click)
frame.add_button("Reset",click2)

# Crea un timer para la simulación,
timer = simplegui.create_timer(1000*dt,tick)

# Abre la ventana
frame.start()