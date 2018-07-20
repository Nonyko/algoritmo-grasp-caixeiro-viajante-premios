from tools import *
from cidadecandidata import *
from rota import *


def main():
    # Lendo arquivos e gerando matriz de distancias
    stringsarquivo = lerarquivo('distancias11.csv')
    ncidades = len(stringsarquivo)
    distancia = criarmatrizdistancia(stringsarquivo, ncidades)
    stringsarquivo = lerarquivo('premios11.csv')
    premios = criarvetorvalores(stringsarquivo, ncidades)
    stringsarquivo = lerarquivo('penalties11.csv')
    penalidades = criarvetorvalores(stringsarquivo, ncidades)


    premiominimo = 295.5
    print(premiominimo)
    # Parametro de quantos elementos vão entrar no sorteio para a solucao
    porcentagemcorte = 0.5

    rotasuperlegal = None


    for interacao in range(0, 500000):

        # GULOSO ALEATORIO

        # Criar vetor de solução novo
        solucaogulosa =solucaogulosaaleatoria(porcentagemcorte, ncidades, distancia,premiominimo, premios)

        caminhobase = Rota(solucaogulosa, distancia, premios, penalidades)# Transformando vetor de solução em rota

        # BUSCA LOCAL E SALVANDO MELHOR SOLUCAO
        if rotasuperlegal is None:
            rotasuperlegal = Rota(caminhobase.caminho.copy(), distancia, premios, penalidades)#Rota super legal é a melhor rota de todas ate agora
            print('it: ' + str(interacao))
            print("Primeira vez:")
            print(rotasuperlegal.caminho)
            print(rotasuperlegal.custo)
        else:
            if rotasuperlegal.custo > caminhobase.custo:
                rotasuperlegal = Rota(caminhobase.caminho.copy(), distancia, premios, penalidades)
                print('it: ' + str(interacao))
                print("Melhorado:")
                print(rotasuperlegal.caminho)
                print(rotasuperlegal.custo)

        caminhobasetrocado = trocarvariasvezes(caminhobase, distancia, ncidades, premios, penalidades)
        if caminhobasetrocado.custo < rotasuperlegal.custo:
            rotasuperlegal = Rota(caminhobasetrocado.caminho.copy(), distancia, premios, penalidades)
            print('it: ' + str(interacao))
            print("Melhorado:")
            print(rotasuperlegal.caminho)
            print(rotasuperlegal.custo)

    print("Caminho Final:")
    print(rotasuperlegal.caminho)
    print(rotasuperlegal.custo)







if __name__ == '__main__':
    main()