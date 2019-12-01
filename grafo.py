class Grafo:
	def __init__(self, nome_arquivo = None):
		self.vizinhos = {}
		self.vertices = []
		self.n = 0
		self.m = 0

		if nome_arquivo is not None:
			self.carregar_do_arquivo(nome_arquivo)

	def add_vertice(self, v):
		if v not in self.vertices:
			self.vizinhos[v] = []
			self.vertices.append(v)
			self.n += 1


	def add_aresta(self, u, v):
		if u != v:
			if u not in self.vertices:
				self.add_vertice(u)
			if v not in self.vertices:
				self.add_vertice(v)

			if v not in self.vizinhos[u]:
				self.m += 1
				self.vizinhos[u].append(v)
				self.vizinhos[v].append(u)

	def carregar_do_arquivo(self, nome_arquivo):
		with open(nome_arquivo, 'r') as arquivo:
			linhas = arquivo.readlines()
			for linha in linhas:
				linha = "".join(linha.split()) #remove todos os whitespaces
				
				if len(linha) == 0:
					continue
				
				adjacencia = linha.split(":") #a string antes do ':' é o vértice em questão e tudo depois do ':' são os vizinhos desse vértice. cada linha representa uma relação de adjacência
				
				if len(adjacencia) == 1:
					self.add_vertice(adjacencia[0]) #nesse caso a linha não tem um ':', portanto é um vértice isolado
				else:
					v = adjacencia[0]
					vizinhos = adjacencia[1].split(',')
					for u in vizinhos:
						if u != "": 
							self.add_aresta(v, u)
						else:
							self.add_vertice(v)  #nesse caso não há nada após o ':', portanto v é um vértice isolado

	def __str__(self):
		string = "vértices = " + str(self.n) + ", arestas = " + str(self.m) + "\n"

		for v in self.vertices:
			string += "N(" + v + ") = {"

			if len(self.vizinhos[v]) == 0:
				string += "}\n"
				continue

			for u in self.vizinhos[v]:
				string += u + ", "
			
			string = string[:-len(", ")] + "}\n"

		return string[:-len("\n")] #remove o último \n
