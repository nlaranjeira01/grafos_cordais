import eficiente, forca_bruta, utils
from grafo import Grafo
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--arquivo", help = "Nome do arquivo que descreve o grafo", default = "entrada.txt")
parser.add_argument("-m", "--metodo", help = "Método para verificar se um grafo é cordal (opções: [fb, forca_bruta]  OU [ef, eficiente])", required = True, choices=["fb", "forca_bruta", "ef", "eficiente"])
args = parser.parse_args()

arquivo = args.arquivo
g = Grafo(arquivo)
print("Grafo carregado:")
print(g)
if args.metodo in {"fb", "forca_bruta"}:
	print("Executando o algoritmo força bruta")
	saida_fb = forca_bruta.eh_cordal_forca_bruta(g)

	if saida_fb[0] == False:
		print("O grafo não é cordal!")
		print(str(saida_fb[1]) + " dos ciclos de tamanho > 3 não contêm cordas")
		print("Subgrafo(s) proibido(s) encontrado(s): ")

		for proibido in saida_fb[2]:
			print(", ".join(proibido))
	else:
		print("O grafo é cordal!")

elif args.metodo in {"ef", "eficiente"}:
	print("Executando o algoritmo eficiente (ordem de eliminação perfeita)")
	saida_ef = eficiente.eh_cordal_LEXBFS(g)

	if saida_ef[0] == False:
		print("O grafo não é cordal!")
		print("Subgrafo proibido encontrado: " + ", ".join(saida_ef[1]))
	else:
		print("O grafo é cordal!")
		print("Ordem de eliminação perfeita: " + ", ".join(saida_ef[1]))