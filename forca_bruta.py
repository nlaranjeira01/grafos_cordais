# -*- coding: utf-8 -*-
from collections import deque
from grafo import Grafo
from utils import conta_memoria

"""
Retorna todos os ciclos cujos tamanhos são maiores que 3
"""
def achar_ciclos4_forca_bruta(G):
	ciclos = [] #variável que contém todos os ciclos únicos encontrados
	for v in G.vertices: #percorremos a partir de cada um dos vértices
		vertice_inicial = v
		pilha = deque() #um conteiner que contém todos os caminhos que iniciam a partir do vértice_inicial (poderia ser qualquer conteiner, na real)
		pilha.append([vertice_inicial]) #o caminho inicial começa com o vértice_inicial

		while pilha: #enquanto a pilha não estiver vazia
			caminho_ate_v = pilha.pop() #removemos algum caminho do conteiner
			v = caminho_ate_v[-1] #último vértice do caminho até o momento

			for u in G.vizinhos[v]: #para continuar o caminho, percorremos os vizinhos do último vértice
				if u == vertice_inicial: #caso um dos vizinhos seja o vertice_inicial, então formamos um ciclo que começa e termina em vertice_inicial
					if len(caminho_ate_v) > 3: #para o problema de grafos cordais (força bruta), queremos apenas os ciclos de tamanho 4 ou maiores
						novo_ciclo = caminho_ate_v
						ciclo_duplicado = any([ciclos_sao_iguais(novo_ciclo, c) for c in ciclos]) #verificamos se o novo ciclo já foi encontrado anteriormente (pode estar permutado)
						
						if not ciclo_duplicado: #se o ciclo é diferente de todos os outros até agora
							ciclos.append(novo_ciclo.copy()) #novo ciclo é adicionado aos ciclos encontrados

				elif u not in caminho_ate_v: #caso o vizinho u seja diferente do vértice inicial, precisamos saber se u já não está no caminho (formaria um ciclo com 'folhas')
					caminho_ate_u = caminho_ate_v[:] #cópia do caminho
					caminho_ate_u.append(u) #vizinho u é adicionado ao novo caminho
					pilha.append(caminho_ate_u) #novo caminho é adicionado na pilha
			conta_memoria()
	return ciclos

"""
Verifica se o ciclo c1 é igual ao ciclo c2 através de algumas permutações (rotação e inversão)
"""
def ciclos_sao_iguais(c1, c2):
	if len(c1) == len(c2): #se os tamanhos dos ciclos não são iguais os ciclos são diferentes
		
		try:
			indice_elem_comum = c2.index(c1[0]) #para poder rotacionar o ciclo c2, é preciso saber a posição de um elemento em comum nos dois ciclos (nesse caso o elemento em comum procurado é o primeiro vértice do ciclo c1)
		except ValueError:
			indice_elem_comum = -1 

		if indice_elem_comum == -1: #não há elementos em comum, logo os ciclos são diferentes
			return False

		c2 = rotacionar_ciclo(c2, indice_elem_comum) #caso o primeiro elemento do ciclo c1 exista em c2, é preciso rotacionar c2 de modo a alinhar esse elemento em comum em ambos os ciclos

		if c1 == c2: #com um elemento em comum alinhado, basta verificar se toda a sequência de vértices é igual
			return True

		#chegando aqui sabemos que há um elemento em comum alinhado na posição 0 em ambos os ciclos, mas o resto da sequência ou não está na mesma ordem ou é realmente diferente
		c2 = inverter_ciclo(c2) #pode ser que a sequencia seja a mesma, mas as direções dos ciclos estejam invertidas, logo a direção do ciclo c2 é invertida
		indice_elem_comum = c2.index(c1[0]) #é necessário novamente encontrar a posição do elemento em comum, mas agora já sabemos que ele existe, então sem try/catch
		c2 = rotacionar_ciclo(c2, indice_elem_comum) #o ciclo c2 é novamente rotacionado para que o elemento em comum esteja na posição 0

		if c1 == c2: #só resta saber se o resto da sequência invertida e rotacionada é igual a c1
			return True

	return False
"""
verifica se um ciclo tem corda
uma corda é qualquer aresta que liga dois vértices de um ciclo, mas não pertence ao ciclo
"""
def tem_corda(G, ciclo):
	tamanho_ciclo = len(ciclo)

	for indice_v, v in enumerate(ciclo):
		for u in G.vizinhos[v]:
			adjacentes_v = [ciclo[indice_v - 1], ciclo[(indice_v + 1) % tamanho_ciclo]]
			if u not in adjacentes_v and u in ciclo:
				conta_memoria()
				return True

	conta_memoria()
	return False

"""
Verifica se o grafo G é cordal
Um grafo é cordal caso cada um dos seus ciclos cujos tamanhos são maiores que 3 possuem uma ou mais cordas
"""
def eh_cordal_forca_bruta(G):
	ciclos = achar_ciclos4_forca_bruta(G)

	proibidos = []
	qtd_sem_corda = 0
	for ciclo in ciclos:
		if not tem_corda(G, ciclo):
			 proibidos.append(ciclo)
			 qtd_sem_corda += 1

	conta_memoria()
	if qtd_sem_corda == 0:
		return  (True, qtd_sem_corda, [])

	return (False, qtd_sem_corda, proibidos)

#rotaciona um ciclo n passos à esquerda
def rotacionar_ciclo(ciclo, n):
	return ciclo[n:] + ciclo[:n]

#inverte a direção do ciclo
def inverter_ciclo(ciclo):
	return ciclo[::-1]
