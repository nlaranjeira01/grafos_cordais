# -*- coding: utf-8 -*-
from grafo import Grafo
from utils import No, ListaDuplamenteEncadeada, Conjunto
from collections import deque
from forca_bruta import tem_corda
import os, psutil

#Um grafo é cordal se e somente se ele possui uma ordem de eliminação perfeita
#Uma busca em largura lexicográfica (Lexicographic Breadth-first Search -- LEXBFS) retorna a ordem de eliminação perfeita de um grafo
#Algoritmo baseado nas notas de aula da University of Waterloo (https://www.cse.iitd.ac.in/~naveen/courses/CSL851/uwaterloo.pdf)
def eh_cordal_LEXBFS(G):
	OEP, OEP_predecessores = busca_largura_lexicografica(G) #OEP = Ordem de Eliminação Perfeita
	eh_cordal, corda_faltando = testar_ordem_eliminacao_perfeita(G, OEP, OEP_predecessores)

	if not eh_cordal:
		return (False, encontrar_ciclo(G, corda_faltando[0], corda_faltando[1]))

	return (True, OEP[::-1])

def testar_ordem_eliminacao_perfeita(G, ordenacao, predecessores):
	test = [] #conjunto de pares de vértices que devem ser testados para verificar se formam aresta
	for i in range(len(G.vertices) - 1, -1, -1): #O(n)
		if predecessores[ordenacao[i]] != []: #O(1)
			u = predecessores[ordenacao[i]][-1] #O(1)
			for w in predecessores[ordenacao[i]]: #para cada vértice na ordenação, verificamos os vizinhos, logo passamos por todas as arestas 2x, então é na ordem de O(n + 2m), considerando o loop exterior
				if u != w: #O(1)
					test.append((u, w)) #O(1)
	
	for u, v in test:
		if u in G.vizinhos[v]:
			continue
		else:
			return (False, (u,v))
	return (True, None)

def busca_largura_lexicografica(G):
	lista_vertices = ListaDuplamenteEncadeada()
	pos_vertices = {}

	for v in G.vertices: #O(n)
		lista_vertices.inserir_fim(v) #O(1)
		pos_vertices[v] = lista_vertices.cauda  #O(1)

	Q = ListaDuplamenteEncadeada([Conjunto(lista_vertices, pos_vertices)])

	localizacao = {v:Q.cabeca.prox for v in G.vertices} #(O(n))
	ordem_eliminacao_perfeita = [] #O(1)
	predecessores = {v:[] for v in G.vertices} #O(n)
	esta_na_oep = {v:False for v in G.vertices} #O(n)

	for i in range(len(G.vertices) - 1, -1, -1):
		v = Q.get_primeiro_no().item.vertices.remover_primeiro_no() #O(1), sempre temos a referência do primeiro conjunto
		del Q.get_primeiro_no().item.pos[v.item] #O(1), remoção de elemento de um dicionário
		if Q.get_primeiro_no().item.vertices.vazia(): #O(1), ListaDuplamenteEncadeada tem um membro que indica se a lista está vazia ou não
			Q.remover_primeiro_no() #O(1)
		ordem_eliminacao_perfeita.append(v.item) #O(1)
		esta_na_oep[v.item] = True #O(1)
		for u in G.vizinhos[v.item]: #O(N(u))
			if not esta_na_oep[u]: #O(1)
				predecessores[u].append(v.item) #O(1)

		del localizacao[v.item] #O(1)

		for w in G.vizinhos[v.item]: #O(N(v))
			try:
				conj_w = localizacao[w] #O(1)
			except:
				continue
			ant_conj_w = conj_w.ant
			if ant_conj_w == Q.cabeca or ant_conj_w.item.label == "" or ant_conj_w.item.label[-1] != chr(i): #O(1), só comparamos 1 char da label ou comparamos com string vazia
				ant_conj_w = No(Conjunto(vertices = ListaDuplamenteEncadeada(), pos = {}, label = conj_w.item.label + chr(i))) #linear no tamanho da string, que normalmente é negligível :)
				Q.inserir_no_antecessor(ant_conj_w, conj_w) #O(1)

			no_w = conj_w.item.pos[w] #O(1)
			conj_w.item.vertices.remover_no(conj_w.item.pos[w]) #O(1)
			del conj_w.item.pos[w] #O(1)
			if conj_w.item.vertices.vazia(): #O(1)
				Q.remover_no(conj_w) #O(1)

			localizacao[w] = ant_conj_w
			ant_conj_w.item.vertices.inserir_fim(no_w)
			ant_conj_w.item.pos[w] = no_w

	return (ordem_eliminacao_perfeita, predecessores)

def caminho_de_u_ate_v(G, u, v, caminho_proibido = []):
	fila = deque()
	fila.append(u)
	pred = {u:None}
	caminho_encontrado = False
	while fila:
		w = fila.popleft()
		for x in G.vizinhos[w]:
			if x not in caminho_proibido:
				pred_x = pred.get(x, None)
				if pred_x is None:
					pred[x] = w
					fila.append(x)
					if x == v:
						fila.clear()
						caminho_encontrado = True
						break

	caminho_uv = []

	if not caminho_encontrado:
		return []

	x = v
	while pred[x] != u:
		caminho_uv.append(pred[x])
		x = pred[x]

	return caminho_uv

def encontrar_ciclo(G, u, v):
	caminhos = []
	while True:
		caminho = caminho_de_u_ate_v(G, u, v, caminho_proibido = [v for caminho in caminhos for v in caminho])
		
		if caminho == []:
			break
		
		caminhos.append(caminho)

	ciclo = []
	for i in range(0,len(caminhos) - 1):
		for j in range(i + 1, len(caminhos)):
			ciclo = [u] + caminhos[i][::-1] + [v] + caminhos[j]
			if not tem_corda(G, ciclo):
				return ciclo

	return []
