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
    translate = (0,0,0)
    
    def __init__(self, x, y, z = 0):    
        self.x = x
        self.y = y
        self.z = z

    def desenhar(self, tela):
        x = self.x
        y = self.y
        # desenhar uma bolinha no ponto
        draw.ellipse(tela,(255,255,255),
                     ((x + self.translate[0]) - 2,(y + self.translate[1]) - 2,
                      4,4))

    def rotacionarZ(self,angulo,ponto,tela):
        p = deAngulo(math.radians(angulo))
        self.add(p)
        '''
        p1 = ponto #00
        p2 = self #50
        p3 = None

        if p1.x > p2.x:
            p3 = Ponto(p1.x,p2.y) #00
        else:
            p3 = Ponto(p2.x,p1.y) #00
        p3.desenhar(tela)

        dp1p3 = p1.distancia(p3)
        dp3p2 = p3.distancia(p2) #5
        p32 = deAngulo(math.radians(angulo),dp1p3)
        p32.add(p1)

        p22 = deAngulo(math.radians(angulo+90),dp3p2)
        p22.add(p32)
        
        self.x,self.y = p22.x,p22.y
        '''
    # calcula a distancia entre o ponto atual e outro
    # retorna a distancia
    def distancia(self, ponto):
        x1 = ponto.x
        y1 = ponto.y
        z1 = ponto.z
        
        x2 = self.x
        y2 = self.y
        z2 = self.z

        r = sqrt(pow(x2-x1,2)+pow(y2-y1,2)+pow(z2-z1,2))

        return r

    # copia ponto atual
    def copiar(self):
        return Ponto(self.x,self.y,self.z)

    # soma o ponto atual com outro ponto
    def add(self, ponto):
        self.x += ponto.x
        self.y += ponto.y
        self.z += ponto.z

    # subtrai o ponto atual com outro ponto
    def sub(self, ponto):
        self.x -= ponto.x
        self.y -= ponto.y
        self.z -= ponto.y

    def div(self, n):
        p = self.copiar()
        p.x /= n
        p.y /= n
        p.z /= n

        return p 

    # retorna o valor de x e y em Dump
    def paraDump(self):
        return (self.x+self.translate[0],self.y+self.translate[1])

    def paraDump3D(self):
        return (self.x+self.translate[0],self.y+self.translate[1],self.z+self.translate[2])

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
    def __init__(self, posicao, tamanho, cor = None):
        self.posicao = posicao
        self.tamanho = tamanho
        self.angulos = Ponto(0,0,0)
        self.centro = Ponto(tamanho.x/2,tamanho.y/2)
        self.centro.add(self.posicao)
        
        self.pontos = self.__gerar_pontos()
        self.cor = (randint(100,255),randint(100,255),randint(100,255))
        
        if cor != None:
            self.cor = cor

    def __gerar_pontos(self):
        raio = self.centro.distancia(self.posicao)
        x , y, z = self.posicao.paraDump3D()
        tx, ty = self.tamanho.paraDump()
        
        p = []
        x_inv = 90
        x_cont = 0
        for i in range(-45,270,90):
            pontoZ = deAngulo(math.radians(i),raio)
            
            #pontoX.add(pontoZ)
            p.append(pontoZ)
        
        p[0].add(self.centro)
        p[1].add(self.centro)
        p[2].add(self.centro)
        p[3].add(self.centro)
        return p

    def rodarZ(self,angulo):
        self.angulos.z = angulo
        for i in range(4):
            cx,cy = self.centro.paraDump()
            x,y = self.pontos[i].paraDump()
            a = math.radians(self.angulos.z)
            nx = cx + (x - cx) * math.cos(a) - (y - cy) * math.sin(a)
            ny = cy + (x - cx) * math.sin(a) + (y - cy) * math.cos(a)
            self.pontos[i].x,self.pontos[i].y = nx,ny
        
        #self.pontos = self.__gerar_pontos()

    def rodarX(self,angulo):
        self.angulos.x = angulo
        for i in range(4):
            cx,cy,cz = self.centro.paraDump3D()
            x,y,z = self.pontos[i].paraDump3D()
            a = math.radians(self.angulos.x)
            ny = cy + (y - cy) * math.cos(a) - (z - cz) * math.sin(a)
            nz = cz + (y - cy) * math.sin(a) + (z - cz) * math.cos(a)
            self.pontos[i].z,self.pontos[i].y = nz,ny

    def rodarY(self,angulo):
        self.angulos.y = angulo
        for i in range(4):
            cx,cy,cz = self.centro.paraDump3D()
            x,y,z = self.pontos[i].paraDump3D()
            a = math.radians(self.angulos.y)
            nx = cx + (x - cx) * math.cos(a) - (z - cz) * math.sin(a)
            nz = cz + (x - cx) * math.sin(a) + (z - cz) * math.cos(a)
            self.pontos[i].z,self.pontos[i].x = nz,nx

    def desenhar(self, tela):
        p = []
        for po in self.pontos:
            p.append(po.paraDump())
        draw.polygon(tela,self.cor,p)
        self.centro.desenhar(tela)

    def moverX(self,n):
        for p in self.pontos:
            p.x += n

    def moverY(self,n):
        for p in self.pontos:
            p.y += n

    def moverZ(self,n):
        for p in self.pontos:
            p.z += n

    def rodarDireita(self):
        self.pontos[0].x = self.pontos[1].x
        self.pontos[0].z = self.tamanho

        self.pontos[3].x = self.pontos[2].x
        self.pontos[3].z = self.tamanho

    def rodarEsquerda(self):
        self.pontos[1].x = self.pontos[0].x
        self.pontos[1].z = self.tamanho

        self.pontos[2].x = self.pontos[3].x
        self.pontos[2].z = self.tamanho

    def rodarCima(self):
        self.pontos[2].y = self.pontos[1].y
        self.pontos[2].z = self.tamanho

        self.pontos[3].y = self.pontos[0].y
        self.pontos[3].z = self.tamanho


class Cubo():
    
    def __init__(self, posicao, tamanho, ide):
        self.posicao = posicao
        self.tamanho = tamanho
        self.centro = None
        self.quadrados = self.__gerar_quadrados()
        self.ide = ide
        
    def __gerar_quadrados(self):
        raios = self.tamanho.div(2)
        t = self.tamanho
        print(raios.paraDump3D())
        r = []

        #base
        r.append(Quadrado(self.posicao, self.tamanho, (255, 0, 0)))
        r[0].centro.z = raios.z
        
        #tras
        r.append(Quadrado(self.posicao, self.tamanho, (255, 255, 255)))
        r[1].rodarX(90)
        r[1].moverY(-raios.y)
        r[1].moverZ(raios.z)

        #frente
        r.append(Quadrado(self.posicao, self.tamanho, (255, 255, 0)))
        r[2].rodarX(90)
        r[2].moverY(raios.y)
        r[2].moverZ(raios.z)

        #esquerda
        r.append(Quadrado(self.posicao, self.tamanho, (0, 0, 255)))
        r[3].rodarY(90)
        r[3].moverX(-raios.x)
        r[3].moverZ(raios.z)

        #direita
        r.append(Quadrado(self.posicao, self.tamanho, (0, 255, 0)))
        r[4].rodarY(90)
        r[4].moverX(raios.x)
        r[4].moverZ(raios.z)

        #cima
        r.append(Quadrado(self.posicao, self.tamanho, (255, 165, 0)))
        r[5].rodarX(180)
        r[5].moverZ(t.z)

        self.centro = r[0].centro
        
        return r

    def removerLado(self,i):
        self.quadrados.remove(self.quadrados[i])

    def desenhar(self,tela):
        for q in self.quadrados:
            q.centro = self.centro
            q.desenhar(tela)

    def rodarX(self,angulo):
        for q in self.quadrados:
            q.centro = self.centro
            q.rodarX(angulo)

    def rodarY(self,angulo):
        for q in self.quadrados:
            q.centro = self.centro
            q.rodarY(angulo)

    def rodarZ(self,angulo):
        for q in self.quadrados:
            q.centro = self.centro
            q.rodarZ(angulo)

    def __str__(self):
        return str(self.ide)









        
