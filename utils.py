from grafo import Grafo


class No:
	def __init__(self, item = None):
		self.item = item
		self.prox = None
		self.ant = None

	def __str__(self):
		return str(self.item)
	def __repr__(self):
		return str(self.item)

class ListaDuplamenteEncadeada:
	def __init__(self, itens = None):
		self.cabeca = No(None)
		self.cauda = self.cabeca
		self.tamanho = 0

		if itens:
			try:
				iter(itens)
			except TypeError:
				raise TypeError("ListaDuplamenteEncadeada não pode ser construída a partir de valores não iteráveis")
			else:
				for item in itens:
					self.inserir_fim(item)

	def inserir_fim(self, item):
		if isinstance(item, No):
			no = item
		else:
			no = No(item)
	
		no.ant = self.cauda
		self.cauda.prox = no
		self.cauda = no
		self.tamanho += 1


	def remover_primeiro_no(self):
		no = None
		if self.cabeca.prox:
			no = self.cabeca.prox
			self.cabeca.prox = self.cabeca.prox.prox
			if not self.cabeca.prox:
				self.cauda = self.cabeca
			else:
				self.cabeca.prox.ant = self.cabeca

			self.tamanho -= 1

		return no

	def remover_no(self, no):
		if no and no.ant and not self.vazia():
			no.ant.prox = no.prox
			if no != self.cauda:
				no.prox.ant = no.ant
			else:
				self.cauda = no.ant
			no.ant = None
			no.prox = None
			self.tamanho -= 1

	def inserir_no_antecessor(self, novo_ant, no):
		if not no or no == self.cabeca:
			return
		novo_ant.prox = no
		novo_ant.ant = no.ant
		no.ant.prox = novo_ant
		no.ant = novo_ant
		self.tamanho += 1


	def get_primeiro_no(self):
		return self.cabeca.prox

	def vazia(self):
		return self.tamanho == 0

	def __str__(self):
		if self.vazia():
			return "[]"

		s = "["
		iterador = self.cabeca

		while iterador.prox:
			s += str(iterador.prox.item) + ","
			iterador = iterador.prox

		s = s[:-1] + "]"
		return s

	def __repr__(self):
		if self.vazia():
			return "[]"

		s = "["
		iterador = self.cabeca

		while iterador.prox:
			s += str(iterador.prox.item) + ","
			iterador = iterador.prox

		s = s[:-1] + "]"
		return s

class Conjunto:
	def __init__(self, vertices = ListaDuplamenteEncadeada(), pos = {}, label = ""):
		self.vertices = vertices
		self.pos = pos
		self.label = label


def grafoCompleto(size):
	if size <= 0:
		raise ValueError("o tamanho do grafo deve ser um número positivo")
	g = Grafo()
	g.add_vertice("0")
	for i in range(1, size):
		for j in g.vertices:
			g.add_aresta(str(i), str(j))
	return g

def grafoNaoCordal(size):
	g = Grafo()
	if(size < 4):
		raise ValueError("Qualquer grafo com menos de 4 vértices é cordal")

	# criando ciclo de tamanho 4 (subgrafo proibido para tornar o grafo não cordal)
	for i in range(0, 4):
		if(i == 3):
			g.add_aresta(str(i), str(0))

		else:
			g.add_aresta(str(i), str(i+1))

	# Inserindo novos vértices considerando o tamanho definido pelo usuário
	for i in range(4, size):
		for j in g.vertices:
			g.add_aresta(str(i), str(j))

	return g

try:
	from guppy import hpy
	hp = hpy()
except:
	hp = None


def var_estatica(var_nome, valor):
	def decorar(func):
		setattr(func, var_nome, valor)
		global hp
		hp.setrelheap()
		return func
	return decorar

@var_estatica("max", 0)
def conta_memoria():
	global hp
	if hp:
		sz = hp.heap().size
		if sz > conta_memoria.max:
			conta_memoria.max = sz
	return conta_memoria.max