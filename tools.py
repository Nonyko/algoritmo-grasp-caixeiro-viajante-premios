import os
from numpy import *
import random
import rota
from copy import copy
import statistics
from fractions import Fraction as F
from decimal import Decimal as D
from cidadecandidata import *
from rota import *



def lerarquivo(nomearquivo):
    ref_arquivo = open(nomearquivo, "r")
    linhas = ref_arquivo.readlines()
    ref_arquivo.close()
    return linhas

def criarmatrizdistancia(stringsarquivo, ncidades):
    matrizdistancia = []
    for l in range(0, ncidades):
        colunas = []
        linhastring = stringsarquivo[l].replace("\n", "").split(';')
        for c in range(0, ncidades):
            colunas.append(linhastring[c])
        matrizdistancia.append(colunas)
    return matrizdistancia

def criarvetorvalores(stringsarquivo, ncidades):
    colunas = []
    linhastring = stringsarquivo[0].replace("\n", "").split(';')
    for c in range(0, ncidades):
        colunas.append(linhastring[c])

    return colunas


def calculacusto(self, caminhoentrada, matrizdistancia, penalidades):
    custo = 0

    # interar i vezes, sendo i o numero de elementos do caminho de entrada-1.
    # Ou seja, i vai receber as posicoes do caminho e caminhoentrada[i] o valor daquela posicao
    for i in range(len(caminhoentrada) - 1):
        custo += float(matrizdistancia[caminhoentrada[i]][caminhoentrada[i + 1]])
    custo += float(matrizdistancia[caminhoentrada[len(caminhoentrada) - 1]][caminhoentrada[0]])
    # calcula o numero de cidades.
    ncidades = len(matrizdistancia)
    penalidade = 0
    # iterar entre 0 e ncidades-1
    for i in range(ncidades):
        if not i in caminhoentrada:  # caso a posicao nao esteja no caminho:
            penalidade += float(penalidades[i])  # adicionar a penalidade daquela posicao
    custo += penalidade  # somar penalidade a custo

    return custo


def printcidadescandidatas(citycands):
    for city in citycands:
        print(str(city.numero) + '[' + str(city.distanciaparacidadeatual) + ']' + ', ', end="")
    print("\n")

def gerarlistacidadescandidatas(ncidades, cidadeinicial,matrizdistancia):
    citycands = []
    for i in range(ncidades):
        if not i==cidadeinicial:
            citycand = CidadeCandidata(i,cidadeinicial, matrizdistancia)
            citycands.append(citycand)


    # Ordenando pela distancia para a distancia atual
    citycands = sorted(citycands, key=lambda CidadeCandidata: CidadeCandidata.distanciaparacidadeatual)
    #printcidadescandidatas(citycands)
    return citycands

def getslicesorteavel(porcentagem,ncidades,citycands):
    porcentagemcorte = porcentagem
    slicesorteavel = int(1 + porcentagemcorte*(len(citycands)-1))
    return slicesorteavel
'''
def getslicesorteavel(porcentagem,ncidades,citycands):
    porcentagemcorte = porcentagem
    slicesorteavel = int(ncidades * porcentagemcorte)

    if slicesorteavel == 0:
        if (len(citycands) > 1):
            slicesorteavel = 2
        else:
            slicesorteavel = 1
    return slicesorteavel
'''
def atualizardistanciaparaatualcitycands(citycands, cidadeatual, matrizdistancia):
    for city in citycands:
        city.atualizardistanciaparacidadeatual(cidadeatual, matrizdistancia)
    return citycands

def solucaogulosaaleatoria(porcentagemcorte, ncidades, distancia, premiominimo, premios):
    # Sorteando a primeira cidade
    #cidadeinicial = random.choice(range(ncidades))
    cidadeinicial = 0
    premioatual = float(premios[0])
    #print(cidadeinicial)

    # Criando uma lista com cidades candidatas.
    citycands = gerarlistacidadescandidatas(ncidades, cidadeinicial, distancia)

    # Vetor de solução
    solucaogulosa = []
    solucaogulosa.append(cidadeinicial)
    # Fazer ate completar solucao
    while len(solucaogulosa) < ncidades and premioatual <= premiominimo:
        # Ver quantas cidades entram no sorteio
        slicesorteavel = getslicesorteavel(porcentagemcorte, ncidades, citycands)
        citycands[:slicesorteavel]
        # Sorteio da nova cidade atual

        cidadeatual = random.choice(citycands[:slicesorteavel])
        # Adicionar cidade sorteada ao vetor de solucao e removê-lo das candida-tas
        premioatual += float(premios[cidadeatual.numero])
        solucaogulosa.append(cidadeatual.numero)
        citycands.remove(cidadeatual)

        # Atualizar lista de distancias para cidade atual e reordenar por essa distância
        citycands = atualizardistanciaparaatualcitycands(citycands, cidadeatual, distancia)
        citycands = sorted(citycands, key=lambda CidadeCandidata: CidadeCandidata.distanciaparacidadeatual)

    return solucaogulosa

def trocarespacoscaminho(caminhobase, indice1, indice2, distancia, premios, penalidades):
    caminhobasefuncao = Rota(caminhobase.caminho.copy(), distancia, premios, penalidades)
    valorauxiliar = caminhobasefuncao.caminho[indice1]
    caminhobasefuncao.caminho[indice1] = caminhobasefuncao.caminho[indice2]
    caminhobasefuncao.caminho[indice2] = valorauxiliar
    # Atualizar custo rota
    caminhobasefuncao = Rota(caminhobasefuncao.caminho, distancia, premios, penalidades)
    return caminhobasefuncao

def trocarvariasvezes(caminhobase, distancia,ncidades, premios, penalidades):
    customelhorvizinho = None
    indice1melhorvizinho = None
    indice2melhorvizinho = None

    melhorou = True

    inicio1 = random.choice(range(ncidades - 1))
    inicio2 = inicio1 + 1
    # Trocar valores
    while melhorou:
        for indice1 in range(0, ncidades-1):
            for indice2 in range(1, ncidades):
                #print('resetando caminho')
                caminhobasetrocado = trocarespacoscaminho(caminhobase, indice1, indice2, distancia, premios, penalidades)
                #print(caminhobasetrocado.caminho)
                #print(caminhobasetrocado.custo)
                #print(caminhobase.caminho)
                #print(caminhobasetrocado.caminho)
                # Atualiza achados melhores
                if customelhorvizinho is None:
                    customelhorvizinho = caminhobasetrocado.custo
                    indice1melhorvizinho = indice1
                    indice2melhorvizinho = indice2

                else:
                    if caminhobasetrocado.custo < customelhorvizinho:
                        customelhorvizinho = caminhobasetrocado.custo
                        indice1melhorvizinho = indice1
                        indice2melhorvizinho = indice2

                    else:
                        melhorou = False
                        break
                    if not melhorou:
                        break
                if not melhorou:
                    break
                '''
                print('melhorvizinho'+str(customelhorvizinho))
                print(indice1melhorvizinho)
                print(indice2melhorvizinho)
                '''
            if not melhorou:
                break
    caminhobasetrocado = trocarespacoscaminho(caminhobase, indice1melhorvizinho, indice2melhorvizinho, distancia, premios, penalidades)

    return caminhobasetrocado