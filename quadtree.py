import numpy as np
import math

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distanciadocentro(self, centro):
        return math.sqrt((centro.x-self.x)**2 + (centro.y-self.y)**2)

class Quadro:
    def __init__(self, centro, largura, altura):
        self.centro= centro
        self.largura = largura
        self.altura = altura
        self.esquerda = centro.x - largura
        self.direita = centro.x + largura
        self.topo = centro.y - altura
        self.base = centro.y + altura

    def contemPonto(self, Ponto):
        return (self.esquerda <= Ponto.x < self.direita and
               self.topo <= Ponto.y <self.base)
    
    def intersecta(self, area):
        return not (area.esquerda > self.direita or
                    area.direita < self.esquerda or
                    area.topo > self.base or
                    area.base < self.topo)

    def desenhar(self, ax, c='k', lw=1, **kwargs):
        x1, y1 =self.esquerda, self.topo
        x2, y2 =self.direita, self.base
        ax.plot([x1,x2,x2,x1,x1], [y1,y1,y2,y2,y1], c=c, lw=lw, **kwargs)


class Quadtree:
    def __init__(self, dimensoes, capacidade =1):
        self.dimensoes = dimensoes
        self.capacidade = capacidade
        self.pontos = []
        self.dividido = False

    def inserir(self, Ponto):
        # caso o Ponto esteja no alcance da quadtree atual
        if not self.dimensoes.contemPonto(Ponto):
            return False
    
        #bd não tiver alcançado a capacidade
        if len(self.pontos) < self.capacidade:
            self.pontos.append(Ponto)
            return True

        if not self.dividido:
            self.dividir()
        
        if self.te.inserir(Ponto):
            return True
        elif self.td.inserir(Ponto):
            return True
        elif self.be.inserir(Ponto):
            return True
        elif self.bd.inserir(Ponto):
            return True

        return False

    def area_de_busca(self, area):
        pontos_encontrados = []

        if not self.dimensoes.intersecta(area):
            return []

        for Ponto in self.pontos:
            if area.contemPonto(Ponto):
                pontos_encontrados.append(Ponto)

        if self.dividido:
            pontos_encontrados.extend(self.te.area_de_busca(area))
            pontos_encontrados.extend(self.td.area_de_busca(area))
            pontos_encontrados.extend(self.be.area_de_busca(area))
            pontos_encontrados.extend(self.bd.area_de_busca(area))

        return pontos_encontrados

    

    def dividir(self):
        centro_x = self.dimensoes.centro.x
        centro_y = self.dimensoes.centro.y
        new_largura = self.dimensoes.largura / 2
        new_altura = self.dimensoes.altura / 2

        te = Quadro(Ponto(centro_x - new_largura, centro_y - new_altura), new_largura, new_altura)
        self.te = Quadtree (te)
        for p in self.pontos:
                if self.te.dimensoes.contemPonto(p):
                    self.te.pontos.append(p)

        td = Quadro(Ponto(centro_x + new_largura, centro_y - new_altura), new_largura, new_altura)
        self.td = Quadtree (td)
        for p in self.pontos:
            if self.td.dimensoes.contemPonto(p):
                self.td.pontos.append(p)

        be = Quadro(Ponto(centro_x - new_largura, centro_y + new_altura), new_largura, new_altura)
        self.be = Quadtree (be)
        for p in self.pontos:
            if self.be.dimensoes.contemPonto(p):
                self.be.pontos.append(p)

        bd = Quadro(Ponto(centro_x + new_largura, centro_y + new_altura), new_largura, new_altura)
        self.bd = Quadtree (bd)
        for p in self.pontos:
            if self.bd.dimensoes.contemPonto(p):
                self.bd.pontos.append(p)

        self.dividido = True

    def __len__(self):
        count = len(self.pontos)
        if self.dividido:
            count += len(self.te) + len(self.td) + len(self.be) + len(self.bd)

        return count

    def desenhar (self, ax):
        self.dimensoes.desenhar(ax)

        if self.dividido:
            self.te.desenhar(ax)
            self.td.desenhar(ax)
            self.bd.desenhar(ax)
            self.be.desenhar(ax)