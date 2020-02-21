from pygame import draw
from random import randint
import math
from math import sqrt, pow

# cria um ponto apartir de um angulo
def deAngulo(angulo,raio=1):
    x = raio*math.cos(angulo-(math.pi/2))
    y = raio*math.sin(angulo-(math.pi/2))
    return Ponto(x,y)

# cria linha apartit de dois pontos
def criarLinhadePonto(p1,p2):
    return Linha(p1.x,p1.y,p2.x,p2.y)

'''
    Ponto:
    representa um vetor
'''
class Ponto():
    translate = (0,0)
    
    def __init__(self, x, y):    
        self.x = x
        self.y = y

    def desenhar(self, tela):
        x = self.x
        y = self.y
        # desenhar uma bolinha no ponto
        draw.ellipse(tela,(255,255,255),
                     ((x + self.translate[0]) - 2,(y + self.translate[1]) - 2,
                      4,4))

    # calcula a distancia entre o ponto atual e outro
    # retorna a distancia
    def distancia(self, ponto):
        x1 = ponto.x
        y1 = ponto.y

        x2 = self.x
        y2 = self.y

        r = sqrt(pow(x2-x1,2)+pow(y2-y1,2))

        return r

    # copia ponto atual
    def copiar(self):
        return Ponto(self.x,self.y)

    # soma o ponto atual com outro ponto
    def add(self, ponto):
        self.x += ponto.x
        self.y += ponto.y

    # subtrai o ponto atual com outro ponto
    def sub(self, ponto):
        self.x -= ponto.x
        self.y -= ponto.y

    # retorna o valor de x e y em Dump
    def paraDump(self):
        return (self.x+self.translate[0],self.y+self.translate[1])

    def __str__(self):
        return str(self.x)+','+str(self.y)


class Linha():
    def __init__(self,x1,y1,x2,y2):
        self.a = Ponto(x1,y1) 
        self.b = Ponto(x2,y2)
        self.cor = self.__cor()

    def __cor(self):
        r = randint(100,255)
        g = randint(100,255)
        b = randint(100,255)
        return (r,g,b)

    # ver se a linha atual craza com outra linha
    # retorna um ponto onde elas se cruzam
    def tocar(self,linha):
        x1 = linha.a.x
        y1 = linha.a.y
        x2 = linha.b.x
        y2 = linha.b.y

        x3 = self.a.x
        y3 = self.a.y
        x4 = self.b.x
        y4 = self.b.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None

        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4))/den
        u = -((x1-x2)*(y1-y3)-(y1-y2)*(x1-x3))/den

        if 0 < t < 1 and u > 0:
            pt = Ponto(x1+t*(x2-x1),
                       y1+t*(y2-y1))
            return pt
        else:
            return None

    # retorna uma copia da linha atual
    def copiar(self):
        return criarLinhadePonto(self.a,self.b)

    # soma os pontos da linha com outro ponto
    def add(self, ponto):
        self.a.add(ponto)
        self.b.add(ponto)

    # subtrai os pontos da linha com outro ponto
    def sub(self, ponto):
        self.a.sub(ponto)
        self.b.sub(ponto)

    def desenhar(self,tela):
        draw.line(tela,self.cor,self.a.paraDump(),self.b.paraDump())

    def __str__(self):
        return str(self.a)+','+str(self.b)

class Quadrado():
    def __init__(self, x, y, tamanho, posicao):
        self.posicao = posicao
        self.pontos = [
            Ponto(x,y),
            Ponto(x+tamanho,y),
            Ponto(x+tamanho,y+tamanho),
            Ponto(x,y+tamanho),
            ]
        self.cor = (randint(100,255),randint(100,255),randint(100,255))

    def desenhar(self, tela):
        p = []
        for po in self.pontos:
            p.append(po.paraDump())
        draw.polygon(tela,self.cor,p)

