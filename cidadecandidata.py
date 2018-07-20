import os

class CidadeCandidata(object):
    def __init__(self, numero, cidadeatual,matrizdistancia):
        self.numero = numero
        self.distanciaparacidadeatual = self.calculacustoentrecidades(cidadeatual, numero, matrizdistancia)

    def calculacustoentrecidades(self,cidadeatual, cidadeacomparar, matrizdistancia):
        custo = float(matrizdistancia[cidadeatual][cidadeacomparar])
        return custo

    def atualizardistanciaparacidadeatual(self, cidadeatual,matrizdistancia):
        self.distanciaparacidadeatual = self.calculacustoentrecidades(cidadeatual.numero, self.numero, matrizdistancia)


