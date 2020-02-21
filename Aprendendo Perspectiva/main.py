import pygame
from pygame.locals import *
from utilitarios import *
from visao import Visao
from time import time

# criando a visao
v = Visao(200,200,5)
v.velocidade = 1

#linha de separacao
l = Linha(400,0,400,400)

#criando quadrados
quadrados = []
for i in range(3):
    for j in range(3):
        quadrados.append(Quadrado(i*15,100+j*15,15,Ponto(i,j)))


pygame.font.init()
font = pygame.font.SysFont('Arial',20)

# mostra fps
fps = 0
cont_fps = 0
tempo = time()

def mostraFps(tela):
    global fps,cont_fps,tempo
    cont_fps+=1
    if time() - tempo >= 1:
        tempo = time()
        fps = cont_fps
        cont_fps = 0
    text = font.render("FPS: "+str(fps),False, (0,0,255))
    tela.blit(text,(0,0))

# area de desenhar na tela
def draw(tela):
    renderizacoes = []
    for q in quadrados:
        q.desenhar(tela)
        p = v.renderizar(q,tela)
        if p != None:
            renderizacoes.append(p)

    for r in renderizacoes:
        pygame.draw.polygon(tela,r['cor'],r['pontos'])

    mostraFps(tela)
    
    v.desenhar(tela)
    l.desenhar(tela)
    
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
            v.rodar(200-event.pos[0])
            pygame.mouse.set_pos(200,200)

    #teclas apertadas
    for k in keys:
        if k == K_UP:
            v.rodar_vertical(-0.5*v.velocidade)
        elif k == K_DOWN:
            v.rodar_vertical(0.5*v.velocidade)
        elif k == K_LEFT:
            v.rodar(-0.5*v.velocidade)
        elif k == K_RIGHT:
            v.rodar(0.5*v.velocidade)
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

    if rodando:
        screen.fill((0,0,0))
        
        draw(screen)
               
        pygame.display.update()
