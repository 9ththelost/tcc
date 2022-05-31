import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from quadtree import Ponto, Quadro, Quadtree

DPI= 72

largura, altura = 600,400
N = int ( input ("numero de Pontos: "))

metodo = int (input("pesquisar uma area [1] ou ao redor de um ponto[2]?: "))


if (metodo == 1):
    centro_x = int ( input("Ponto inicial horizontal: "))
    centro_y = int (input("Ponto inicial vertical: "))

    area_largura = int (input("distancia horizontal: "))
    area_altura = int (input("distancia vertical: "))

elif (metodo == 2):
        ponto_ref = int (input("qual ponto "))

        area_largura = int (input("distancia horizontal: "))
        area_altura = int (input("distancia vertical: "))

elif (metodo != 1) and (metodo != 2):
    print("modo invalido")


# gerar alcance aleatorio
#centro_x = np.random.rand() * largura 
#centro_y = np.random.rand() * altura

#utilizar area aleatoria de procura
#np.random.rand() * min(centro_x, largura - centro_x)
#np.random.rand() * min(centro_y, altura - centro_y)

#criar pontos em areas aleatorias
xs = np.random.rand(N) * largura
ys = np.random.rand(N) * altura
particulas = [Ponto(xs[i], ys[i]) for i in range(N)]



espaco = Quadro(Ponto(largura/2, altura/2), largura/2, altura/2)
qtree = Quadtree(espaco)



for ponto in particulas:
    qtree.inserir(ponto)



#desenhar retangulo
fig = plt.figure(figsize=(700/DPI, 500/DPI), dpi=DPI)
ax = plt.subplot()
ax.set_xlim(0, largura)
ax.set_ylim(0, altura)
qtree.desenhar(ax)

#desenhar Pontos
ax.scatter([p.x for p in particulas], [p.y for p in particulas], s=4)
ax.set_xticks([])
ax.set_yticks([])



Pontos_encontrados = []

if (metodo == 1):
    area = Quadro(Ponto(centro_x, centro_y), area_largura, area_altura)
    Pontos_encontrados = qtree.area_de_busca(area)
    

elif (metodo == 2):
    area = Quadro(particulas[ponto_ref], area_largura, area_altura)
    Pontos_encontrados = qtree.area_de_busca(area)
    

print('Pontos no alcance:', len(Pontos_encontrados))

ax.scatter([p.x for p in Pontos_encontrados], [p.y for p in Pontos_encontrados],
            facecolors='none', edgecolors='r', s=32)

area.desenhar(ax, c='r', lw=2)

ax.invert_yaxis()
plt.tight_layout()
plt.savefig('search-quadtree.png', DPI=72)
plt.show()