import random
import numpy

tam_populacao = 10 	#N de individuos na populacaoulacao: 10
tx_c = 0.9	#Taxa de cruzamento
tx_m = 0.01 #Taxa de mutacao
custao = 30
selecionados = []
new_populacao = []

def funcaodecusto(populacao,individuo,matrix): # Funcaoo de Custo de cada individuo
	custo = 0
	for x in range(5):
		if(x != 4):
			custo += matrix[int(populacao[individuo][x])][int(populacao[individuo][x+1])]
		for y in range(5):
			if(populacao[individuo][x] == populacao[individuo][y] and x != y):
				custo += custao
	return custo



def init_populacao(): #Iniciando uma populacaoulacao
	populacao_t = random.sample(range(0, 5), 5)
	for x in range(9):
		#sorteia mais 5 os vertices
		individuo = random.sample(range(0, 5), 5)
		populacao_t = numpy.r_[populacao_t,individuo]
	populacao = numpy.zeros((10,5))
	for x in range(tam_populacao):

		for y in range(5):
			populacao[x][y] = populacao_t[x*5+y]
	return populacao

#Selecao
def selecao(populacao,matrix):
	#roleta
	summ = 0.
	c_ind = [0,0,0,0,0,0,0,0,0,0]
	for i in range(10):
		c_ind[i] = 1./funcaodecusto(populacao,i,matrix)
		summ += 1./funcaodecusto(populacao,i,matrix)
	p_tot = 1
	for i in range(10):
		c_ind[i] = ((c_ind[i])/summ)
	while (len(selecionados) < 6) :
		lucky = random.uniform(0,1)
		for element in c_ind:
			if(lucky < element):
				pai = c_ind.index(element)
				selecionados.append(pai)
				break
			else:
				lucky -= element


#mutacao
def mutacao(filho1):
	mutacao  = random.uniform(0,1)
	if(mutacao < tx_m):
		aux = filho1[0]
		filho1[0] = filho1[4]
		filho1[4] = aux
	return filho1

def intercalarlista(lista1,lista2):
	i = 0
	pais = numpy.zeros(10)
	while(i < 5):
			pais[2*i] = lista1[i]
			pais[2*i+1] = lista2[i]
			i += 1
	return pais	

#Cruzamento
def cruzamento(selecionados,populacao):
	new_populacao = []
	filho = []
	filho2 = []
	k = 0
	while k < tam_populacao:
		cruzamento = random.uniform(0,1)
		if(cruzamento <= tx_c):
			while(len(new_populacao) < 10):
				pai1,pai2 = random.sample(selecionados,2)
				pai1 = populacao[pai1]
				pai2 = populacao[pai2]
				pais = intercalarlista(pai1,pai2)
				for i in pais:
					if(i in filho):
						filho2.append(i)
					else:
						filho.append(i) 	
				filho1 = mutacao(filho)
				filho2 = mutacao(filho2)
				k += 2 		
				new_populacao.append(filho)
				new_populacao.append(filho2)				
				filho2 = []
				filho = []
	return new_populacao
#Calcula custos 
def calcula_custos(populacao):
	custos = []
	j = 0
	while j < tam_populacao:
		custos.append(funcaodecusto(populacao,j , matrix))
		j += 1
	j = 0
	return custos
#Atualiza populacao
#Criar tupla, individuo custo e ordenar por custo
def atualizacao(new_populacao,populacao):
	populacaof = []
	custos_populacao = list(calcula_custos(populacao))
	custos_nova_populacao = list(calcula_custos(new_populacao))
	#------------ Selecionando a elite da velha populacao
	melhorind1 = custos_populacao.index(min(custos_populacao))
	melhorindividuo1 = populacao[melhorind1]
	populacaof.append(list(melhorindividuo1))
	del custos_populacao[melhorind1]
	#------------- 
	populacaosemmelhor = numpy.delete(populacao,melhorind1,0)
	melhorind2 = custos_populacao.index(min(custos_populacao))	
	melhorindividuo2 = populacao[melhorind2]
	populacaof.append(list(melhorindividuo2))
	del custos_populacao[melhorind2]
	#---------------- Selecionando os melhores individuos da nova populacao
	custos_indices = zip(new_populacao,custos_nova_populacao)
	custos_indices = sorted(custos_indices,key = lambda tup: tup[1])
	for j in custos_indices:
		if(len(populacaof) == 10):
			break
		populacaof.append(list(j[0]))
	return populacaof

if __name__ == '__main__':
	#Representacao matricial do grafo(matriz(x,y) onde x e y sao vertices do grafo)
	matrix = numpy.matrix = ([[-1,2,9,3,5],[2,-1,4,3,8],[9,4,-1,7,3],[3,3,7,-1,3],[5,8,3,3,-1]])
	#inicio
	solucao = []
	iteracoes = 0 
	populacao = init_populacao()
	while(iteracoes < 500):
		#Adaptacao
		custos = calcula_custos(populacao)
		#selecao
		selecao(populacao,matrix)
		#Cruzamento
		new_populacao = cruzamento(selecionados,populacao)
		#Atualizacao
		populacao = atualizacao(new_populacao,populacao)
		iteracoes += 1
	custos = calcula_custos(populacao)
	embelezando_solucao = populacao[custos.index(min(custos))]
	for i in embelezando_solucao:
		i = int(i+1)
		solucao.append(i)

	print("solucao: " + str(solucao) + " , custando: " + str(custos[custos.index(min(custos))]))