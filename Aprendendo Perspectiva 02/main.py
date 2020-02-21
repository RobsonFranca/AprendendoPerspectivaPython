import pygame
from pygame.locals import *
from utilitarios import *
from visao import Visao
from time import time
from random import random,randint,choice

import math

# criando a visao
v = Visao(270,270,10)
v.velocidade = 1
v.rodar(-90)

#linha de separacao
l = Linha(400,0,400,400)

c1 = Cubo(Ponto(190,190,0),Ponto(10,10,10),1)
c1.removerLado(4)
c1.removerLado(4)
c1.removerLado(2)

c2 = Cubo(Ponto(200,190,0),Ponto(10,10,10),2)
c2.removerLado(3)
c2.removerLado(4)
c2.removerLado(2)

c3 = Cubo(Ponto(200,190,10),Ponto(10,10,10),3)
c3.removerLado(3)
c3.removerLado(0)
c3.removerLado(1)

c4 = Cubo(Ponto(190,190,10),Ponto(10,10,10),4)
c4.removerLado(4)
c4.removerLado(0)
c4.removerLado(1)

c5 = Cubo(Ponto(190,200,10),Ponto(10,10,10),5)
c5.removerLado(4)
c5.removerLado(0)
c5.removerLado(0)

c6 = Cubo(Ponto(200,200,10),Ponto(10,10,10),6)
c6.removerLado(3)
c6.removerLado(0)
c6.removerLado(0)

c7 = Cubo(Ponto(200,200,0),Ponto(10,10,10),7)
c7.removerLado(3)
c7.removerLado(4)
c7.removerLado(1)

c8 = Cubo(Ponto(190,200,0),Ponto(10,10,10),8)
c8.removerLado(4)
c8.removerLado(4)
c8.removerLado(1)

cubos = [c1,c2,c3,c4,c5,c6,c7,c8]
centro = c1.centro.copiar()
centro.add(Ponto(5,5,5))
for c in cubos:
    c.centro = centro

matriz = [
    [[c1,c2],[c4,c3]],
    [[c8,c7],[c5,c6]],
    ]

pygame.font.init()
font = pygame.font.SysFont('Arial',20)

angulos = Ponto(0,0,0)

# mostra fps
fps = 0
cont_fps = 0
tempo = time()
pause = False

def mostraFps(tela):
    global fps,cont_fps,tempo
    cont_fps+=1
    if time() - tempo >= 1:
        tempo = time()
        fps = cont_fps
        cont_fps = 0
    text = font.render("FPS: "+str(fps),False, (0,0,255))
    tela.blit(text,(0,0))

lado = None
cont_a = 0
dirs = [-3,3]
dir_a = None
eixos = ['x','y','z']
eixo = None
lad = 0

def escolherLado(eixo,n):
    global matriz
    r = []
    for p in range(2):
        #print('\n/')
        for l in range(2):
            #print('')
            for c in range(2):
                #print(matriz[p][l][c],end=',')
                if eixo == 'y':
                    if p == n:
                        r.append(matriz[p][l][c])
                if eixo == 'z':
                    if l == n:
                        #print(matriz[p][l][c])
                        #print(p,l,c)
                        #matriz[p][l][c].rodarZ(40)
                        r.append(matriz[p][l][c])
                if eixo == 'x':
                    if c == n:
                        r.append(matriz[p][l][c])
    
    r[2],r[3] = r[3],r[2]
    return r

def trocarLado(eixo,n,r,dir_a):
    global matriz
    if eixo != 'x':
        if dir_a > 0:
            p = r[3]
            for i in range(len(r)-2,-1,-1):
                r[i+1]=r[i]
            r[0]=p
        else:
            p = r[0]
            for i in range(1,len(r)):
                r[i-1]=r[i]
            r[3] = p
    else:
        if dir_a < 0:
            p = r[3]
            for i in range(len(r)-2,-1,-1):
                r[i+1]=r[i]
            r[0]=p
        else:
            p = r[0]
            for i in range(1,len(r)):
                r[i-1]=r[i]
            r[3] = p

    
    r[2],r[3] = r[3],r[2]
    
    i = 0
    for p in range(2):
        for l in range(2):
            for c in range(2):
                if eixo == 'y':
                    if p == n:
                        matriz[p][l][c] = r[i]
                        i+=1
                elif eixo == 'z':
                    if l == n:
                        matriz[p][l][c] = r[i]
                        i+=1
                elif eixo == 'x':
                    if c == n:
                        matriz[p][l][c] = r[i]
                        i+=1

teste = 0
seq = [('x',0),#('x',0),#('x',0),('x',0),
       ('z',0),('x',0),('y',0)]

# area de desenhar na tela
def draw(tela):
    global cont_a,dirs,dir_a,lado,eixo,lad,pause,teste,matriz
    renderizacoes = []

    if lado == None:
        lad = randint(0,1)
        eixo = choice(eixos)
        lado = escolherLado(eixo,lad)
        cont_a = 0
        dir_a = choice(dirs)
        
    if not pause:
        for c in lado:
            if eixo == 'x':
                c.rodarX(dir_a)
                cont_a+=dir_a
            elif eixo == 'y':
                c.rodarY(dir_a)
                cont_a+=dir_a
            elif eixo == 'z':
                c.rodarZ(dir_a)
                cont_a+=dir_a

    if not -360<cont_a<360:
        trocarLado(eixo,lad,lado,dir_a)
        lado = None

    for c in cubos:
        c.desenhar(tela)
        
        for q in c.quadrados:
            p = v.renderizar(q,tela)
            if p != None:
                renderizacoes.append(p)
            
    for i in range(len(renderizacoes)):
        for j in range(i+1,len(renderizacoes)):
            if renderizacoes[i]['distancia'] < renderizacoes[j]['distancia']:
                renderizacoes[i],renderizacoes[j] = renderizacoes[j],renderizacoes[i]
    
    for r in renderizacoes:
        pygame.draw.polygon(tela,r['cor'],r['pontos'])
        for i in range(len(r['pontos'])):
            pygame.draw.line(tela,(0,0,0),r['pontos'][i],r['pontos'][i-1], 2)

    mostraFps(tela)
    
    v.desenhar(tela)
    l.desenhar(tela)
    centro.desenhar(tela)
    
# iniciando pygame
pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('vetor')
pygame.mouse.set_visible(False)

# lista de teclas que estao sendo apertadas
keys = []

# estado do programa
rodando = True

while rodando:
    # pegando eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False
            pygame.quit()
        elif event.type == KEYDOWN:
            keys.append(event.key)
        elif event.type == KEYUP:
            keys.remove(event.key)
        elif event.type == MOUSEMOTION:
            pass
            #v.rodar(200-event.pos[0])
            #pygame.mouse.set_pos(200,200)

    #teclas apertadas
    for k in keys:
        #print(k)
        if k == K_UP:
            v.rodar_vertical(-0.5*v.velocidade)
        elif k == K_DOWN:
            v.rodar_vertical(0.5*v.velocidade)
        elif k == K_LEFT:
            v.rodar(-v.velocidade)
        elif k == K_RIGHT:
            v.rodar(v.velocidade)
        elif k == 97:
            v.esquerda()
        elif k == 100:
            v.direita()
        elif k == 119:
            v.frente()
        elif k == 115:
            v.tras()
        elif k == 113:
            rodando = False
            pygame.quit()
        elif k == 32:
            v.altura.add(Ponto(0,v.velocidade))
            #pause = not pause
        elif k == 304:
            v.altura.add(Ponto(0,-v.velocidade))

    if rodando:
        screen.fill((0,0,0))
        
        draw(screen)
               
        pygame.display.update()
