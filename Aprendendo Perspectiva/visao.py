from utilitarios import *
from math import radians

'''
    
'''
class Visao():
    def __init__(self, x, y, altura = 0):
        self.corpo = Ponto(x,y)
        #self.posicao = Ponto(0,0) ::teste

        '''Definindo angulo da visao'''
        self.angulo_horizontal = 0
        self.angulo_vertical = 90

        '''
            Definindo linhas onde sera montada as perspectivas
            seguindo seus pontos
        '''
        #linha horizontal
        self.p1 = deAngulo(radians(-45),55)
        self.p2 = deAngulo(radians(45),55)
        self.linha_horizontal = Linha(self.p1.x,self.p1.y,
                                      self.p2.x,self.p2.y)
        #linha vertical
        self.p3 = deAngulo(radians(self.angulo_vertical-45),55)
        self.p4 = deAngulo(radians(self.angulo_vertical+45),55)
        self.linha_vertical = Linha(self.p3.x,self.p3.y,
                                    self.p4.x,self.p4.y)

        '''
            Tela é o tamanho da linha horizontal,
            com ela, sabemos onde posicionar o
            objeto na tela de renderizacao
        '''
        self.tela = self.p1.distancia(self.p2)
        self.meio = self.tela/2

        '''
            Definindo um ponto de altura, como ele,
            faremos o calculo de profundidade do objeto
        '''
        self.altura = Ponto(0,self.meio+altura)

        # velocidade de movimento
        self.velocidade = 0.1

        #direcoes
        self.direcao = deAngulo(radians(0))
        self.dir_esquerda = deAngulo(radians(-90))
        self.dir_direita = deAngulo(radians(90))

    '''
        Desenha o objeto visao,
        copo representa um ponto
    '''
    def desenhar(self,tela):
        self.corpo.desenhar(tela)

        '''
            Copia a linha horizontal para poder somar
            com os pontos representado pelo corpo,
            isso mantem a linha se movendo junto do corpo
        '''
        l_aux = self.linha_horizontal.copiar()
        l_aux.add(self.corpo)
        l_aux.desenhar(tela)

    '''
        rotaciona a linha horizontal
    '''
    def rodar(self, n):
        # rotacionando linha
        self.angulo_horizontal += n*(self.velocidade/2)
        self.p1 = deAngulo(radians(-45+self.angulo_horizontal),55)
        self.p2 = deAngulo(radians(45+self.angulo_horizontal),55)
        self.linha_horizontal = Linha(self.p1.x,self.p1.y,
                                      self.p2.x,self.p2.y)

        #rotacionando direcoes
        self.direcao = deAngulo(radians(self.angulo_horizontal))
        self.dir_esquerda = deAngulo(radians(-90+self.angulo_horizontal))
        self.dir_direita = deAngulo(radians(90+self.angulo_horizontal))

    '''
        rotacionar a linha vertical,
        levantar ou abaixar a cabeca
    '''
    def rodar_vertical(self, n):
        self.angulo_vertical += n
        self.p3 = deAngulo(radians(self.angulo_vertical-45),55)
        self.p4 = deAngulo(radians(self.angulo_vertical+45),55)
        self.linha_vertical = Linha(self.p3.x,self.p3.y,
                                    self.p4.x,self.p4.y)

    ''' area de movimentacao '''
    def frente(self):
        self.corpo.x += self.direcao.x*self.velocidade
        self.corpo.y += self.direcao.y*self.velocidade

    def tras(self):
        self.corpo.x -= self.direcao.x*self.velocidade
        self.corpo.y -= self.direcao.y*self.velocidade

    def direita(self):
        self.corpo.x += self.dir_direita.x*self.velocidade
        self.corpo.y += self.dir_direita.y*self.velocidade

    def esquerda(self):
        self.corpo.x += self.dir_esquerda.x*self.velocidade
        self.corpo.y += self.dir_esquerda.y*self.velocidade
    ''' fim area movimentacao '''


    ''' Local onde renderiza a visao com perspectiva '''
    '''
        Entra com um objeto
        Pega os 4 pontos
        Faz os calculos
        Retorna pontos novos em relacao a perspectiva
    '''
    def renderizar(self, objeto, tela):
        pontos = [] #pontos de retorno

        #percorrer os pontos
        for p in objeto.pontos:
            #cria linha entre o copo e o ponto visivel
            l = criarLinhadePonto(self.corpo, p)
            #l.desenhar(tela) #descomente essa linha para ver a linha

            '''
                Copia a linha horizontal para poder somar
                com os pontos representado pelo corpo,
                isso mantem a linha se movendo junto do corpo
            '''
            l_aux = self.linha_horizontal.copiar()
            l_aux.add(self.corpo)

            #vendo se a linha criada cruza com a linha horizontal
            #caso cruze, retorna o ponto onde teve o cruzamento
            ponto = l.tocar(l_aux)

            if ponto != None:
                '''
                    descomente essa linha para poder ver o ponto
                    onde as linhas se cruzam
                ''' 
                # ponto.desenhar(tela)
                ''''''

                #pegar um dos pontos da linha horizontal para medir
                #a distancia entre ela e o poto
                p1_aux = l_aux.a

                # calculo de regra de 3 basica para saber a posicao
                # do ponto de retorno na tela de renderizacao
                '''
                    400 => self.tela
                     x  => p1_aux.distancia(ponto)
                '''
                x = 400+(p1_aux.distancia(ponto)*400)/self.tela

                ''' calculando o eixo y '''
                # pegando a distancia entre o copor e o ponto do objeto
                distancia = p.distancia(self.corpo)

                # criando um ponto para ele
                posicao_ponto = Ponto(distancia,0)
                # criando linha entre o "olho" e o ponto 
                linha = criarLinhadePonto(self.altura,posicao_ponto)

                # adicionando altura a linha vertical
                aux_vert = self.linha_vertical.copiar()
                aux_vert.add(self.altura)

                # pegando onde a linha vertical e a linha
                # entre o "olho" e o ponto se cruzam
                ponto_toque = linha.tocar(aux_vert)
                
                if ponto_toque != None:
                    #regra de 3 basica para saber a altura do ponto
                    '''
                        400 => self.tela
                         x  => aux_vert.a.distancia(ponto_toque)
                    '''
                    y = 400-(aux_vert.a.distancia(ponto_toque)*400)/self.tela
                    ponto.x = x
                    ponto.y = y
                    pontos.append(ponto.paraDump())

        # caso tenha 2 pontos ou menos, nao é posivel criar uma forma
        if len(pontos) > 2:
            return {'pontos':pontos,'cor':objeto.cor}
        
