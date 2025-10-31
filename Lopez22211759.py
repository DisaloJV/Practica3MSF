"""
Práctica 1: Diseño de controladores

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Diego Saul Lopez Islas
Número de control: 22211759
Correo institucional: L22211759@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl
from scipy import signal
import pandas as pd

x0,t0,tend,dt,w,h = 0,0,10,1E-3,10,5
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u= np.zeros(N); u[round(1/dt):round(2/dt)]=1


def musc(a,Cs,R,Cp):
    num = [Cs*R,1-a]
    den = [R*(Cp+Cs),1]
    sys = ctrl.tf(num,den)
    return sys
#Función de transferencia: Control
a,Cs,R,Cp = 0.25,10E-6,100,100E-6
syscontrol = musc(a,Cs,R,Cp)
print(f'Función de transferencia del Control: {syscontrol}')

#Función de transferencia: Caso
a,Cs,R,Cp = 0.25,10E-6,10E3,100E-6
syscaso = musc(a,Cs,R,Cp)
print(f'Función de transferencia del caso: {syscaso}')
_,Fs1 = ctrl.forced_response(syscontrol,t,u,x0)
_,Fs2 = ctrl.forced_response(syscaso,t,u,x0)


fg1 = plt.figure()
plt.plot(t,u,'-',linewidth=1,color=[0.902,0.224,0.274],label='Fs(t)')
plt.plot(t,Fs1,'-',linewidth=1,color=[0.659,0.855,0.863],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth=1,color=[0.271,0.482,0.616],label='Fs1(t):Caso')
plt.grid(False) #Se le pone True en caso de querer la cuadricula
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.4); plt.yticks(np.arange(-0.1,1.6,0.2))
plt.xlabel('t(s)')
plt.ylabel('F(s)[V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('sistema musculoesqueletico python.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema musculoesqueletico python.pdf')


def controlador(kP,kI,sys):
  Cr = 1E-6
  Re = 1/(kI*Cr)
  Rr = kP*Re
  numPI = [Rr*Cr,1]
  denPI = [Re*Cr,0]
  PI = ctrl.tf(numPI,denPI)
  X = ctrl.series(PI,sys)
  sysPI = ctrl.feedback(X,1,sign=-1)
  return sysPI

casoPID = controlador(161.719090452111,21380080.649678,syscaso)

#respuestas en lazo cerrado
_,Fs3 = ctrl.forced_response(casoPID,t,Fs1,x0)

fg2 = plt.figure()
plt.plot(t,u,'-',linewidth=1,color=[0.902,0.224,0.274],label='Fs(t)')
plt.plot(t,Fs1,'-',linewidth=1,color=[0.659,0.855,0.863],label='Fs1(t):Control')
plt.plot(t,Fs2,'-',linewidth=1,color=[0.271,0.482,0.616],label='Fs2(t):Caso')
plt.plot(t,Fs3,'--',linewidth=1.5,color=[0.114,0.208,0.341],label='Fs3(t):Tratamiento')
plt.grid(False) #Se le pone True en caso de querer la cuadricula
plt.xlim(0,10); plt.xticks(np.arange(0,11,1))
plt.ylim(-0.1,1.4); plt.yticks(np.arange(-0.1,1.6,0.2))
plt.xlabel('t(s)')
plt.ylabel('F(s)[V]')
plt.legend(bbox_to_anchor=(0.5,-0.2),loc='center',ncol=3)
plt.show()
fg1.set_size_inches(w,h)
fg1.tight_layout()
fg1.savefig('sistema musculoesqueletico python caso PID.png',dpi=600,bbox_inches='tight')
fg1.savefig('sistema musculoesqueletico python caso PID.pdf')

