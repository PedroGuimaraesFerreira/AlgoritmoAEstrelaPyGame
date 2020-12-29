# pip install pygame
import pygame
import math
from queue import PriorityQueue
import cores

# --> Definir tamanho do lado da janela e o que será escrito no cabeçalho
LADO = 800
JANELA = pygame.display.set_mode((LADO, LADO))
pygame.display.set_caption("Busca de Caminho Mínimo  |  Algoritmo A*")


class Local:
    def __init__(self, linha, coluna, lado, total_linhas):
        self.linha = linha
        self.coluna = coluna
        self.x = linha * lado
        self.y = coluna * lado
        self.cor = cores.BRANCO
        self.vizinhos = []
        self.lado = lado
        self.total_linhas = total_linhas

    # --> Métodos para checar o status de um objeto Local
    def obter_posicao(self):
        return self.linha, self.coluna

    def fechado(self):
        return self.cor == cores.VERMELHO

    def aberto(self):
        return self.cor == cores.VERDE

    def barreira(self):
        return self.cor == cores.PRETO

    def comeco(self):
        return self.cor == cores.LARANJA

    def final(self):
        return self.cor == cores.TURQUESA

    # --> Métodos para modificar o status de um objeto Local
    def reiniciar(self):
        self.cor = cores.BRANCO

    def tornar_comeco(self):
        self.cor = cores.LARANJA

    def tornar_fechado(self):
        self.cor = cores.VERMELHO

    def tornar_aberto(self):
        self.cor = cores.VERDE

    def tornar_barreira(self):
        self.cor = cores.PRETO

    def tornar_final(self):
        self.cor = cores.TURQUESA

    def tornar_caminho(self):
        self.cor = cores.ROXO

    def desenhar(self, janela):
        pygame.draw.rect(janela, self.cor, (self.x, self.y, self.lado, self.lado))

    def atualizar_vizinhos(self, grade):
        self.vizinhos = []

        # checar se é possível descer (não estar no limite da janela e não ser barreira)
        if (
            self.linha < self.total_linhas - 1
            and not grade[self.linha + 1][self.coluna].barreira()
        ):
            self.vizinhos.append(grade[self.linha + 1][self.coluna])

        # checar se é possível subir (não estar no limite da janela e não ser barreira)
        if self.linha > 0 and not grade[self.linha - 1][self.coluna].barreira():
            self.vizinhos.append(grade[self.linha - 1][self.coluna])

        # checar se é possível ir para a direita (não estar no limite da janela e não ser barreira)
        if (
            self.coluna < self.total_linhas - 1
            and not grade[self.linha][self.coluna + 1].barreira()
        ):
            self.vizinhos.append(grade[self.linha][self.coluna + 1])

        # checar se é possível ir para a esquerda (não estar no limite da janela e não ser barreira)
        if self.linha > 0 and not grade[self.linha][self.coluna - 1].barreira():
            self.vizinhos.append(grade[self.linha][self.coluna - 1])

    def __lt__(self, outro):
        return False


# calcular a distância entre os pontos p1 e p2 (em L)
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# após execução do algoritmo e obtenção do caminha mínimo
# traçar/desenhar efetivamente o caminho entre os dois pontos
def reconstruir_caminho(origens, atual, desenhar):
    while atual in origens:
        atual = origens[atual]
        atual.tornar_caminho()
        desenhar()


# inteligência por trás das tomadas de decisão do programa
def algoritmo_a_estrela(desenhar, grade, inicio, final):
    cont = 0
    conjunto_aberto = PriorityQueue()
    conjunto_aberto.put((0, cont, inicio))
    origens = {}

    custo_g = {local: float("inf") for linha in grade for local in linha}
    custo_g[inicio] = 0

    custo_f = {local: float("inf") for linha in grade for local in linha}
    custo_f[inicio] = h(inicio.obter_posicao(), final.obter_posicao())

    conjunto_aberto_hash = {inicio}

    while not conjunto_aberto.empty():
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

        atual = conjunto_aberto.get()[2]
        conjunto_aberto_hash.remove(atual)

        if atual == final:
            reconstruir_caminho(origens, final, desenhar)
            final.tornar_final()
            return True

        for vizinho in atual.vizinhos:
            custo_g_temp = custo_g[atual] + 1

            if custo_g_temp < custo_g[vizinho]:
                origens[vizinho] = atual
                custo_g[vizinho] = custo_g_temp
                custo_f[vizinho] = custo_g_temp + h(
                    vizinho.obter_posicao(), final.obter_posicao()
                )

                if vizinho not in conjunto_aberto_hash:
                    cont += 1
                    conjunto_aberto.put((custo_f[vizinho], cont, vizinho))
                    conjunto_aberto_hash.add(vizinho)
                    vizinho.tornar_aberto()

        desenhar()

        if atual != inicio:
            atual.tornar_fechado()

    return False


def construir_grade(linhas, lado):
    grade = []
    abertura = lado // linhas

    for i in range(linhas):
        grade.append([])
        for j in range(linhas):
            local = Local(i, j, abertura, linhas)
            grade[i].append(local)

    return grade


def desenhar_grade(janela, linhas, lado):
    abertura = lado // linhas
    for i in range(linhas):
        pygame.draw.line(janela, cores.CINZA, (0, i * abertura), (lado, i * abertura))
        for j in range(linhas):
            pygame.draw.line(
                janela, cores.CINZA, (j * abertura, 0), (j * abertura, lado)
            )


def desenhar(janela, grade, linhas, lado):
    janela.fill(cores.BRANCO)

    for linha in grade:
        for local in linha:
            local.desenhar(janela)

    desenhar_grade(janela, linhas, lado)

    # atualizar o desenhado até agora
    pygame.display.update()


def obter_posicao_clique(pos, linhas, lado):
    abertura = lado // linhas
    y, x = pos

    linha = y // abertura
    coluna = x // abertura

    return linha, coluna


# --> loop principal de execução do programa
def main(janela, lado):
    LINHAS = 50
    grade = construir_grade(LINHAS, lado)

    inicio = None
    final = None

    em_execucao = True

    while em_execucao:
        desenhar(janela, grade, LINHAS, lado)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                em_execucao = False

            # quando o botão esquerdo é pressionado
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                linha, coluna = obter_posicao_clique(pos, LINHAS, lado)
                local = grade[linha][coluna]

                # se as posicoes de inicio e final ainda não foram definidas
                # elas serão as primeiras a serem definidas ao clicar
                if not inicio and local != final:
                    inicio = local
                    inicio.tornar_comeco()
                elif not final and local != inicio:
                    final = local
                    final.tornar_final()

                # inicio e final definidos, podemos então desenhar as barreiras
                elif local != inicio and local != final:
                    local.tornar_barreira()

            # quando o botão direito é pressionado (apagar)
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                linha, coluna = obter_posicao_clique(pos, LINHAS, lado)
                local = grade[linha][coluna]
                local.reiniciar()

                if local == inicio:
                    inicio = None
                elif local == final:
                    final = None

            # esperar o usuario apertar a barra de espaco e comecar a rodar o algoritmo
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and inicio and final:
                    for linha in grade:
                        for local in linha:
                            local.atualizar_vizinhos(grade)
                    # desenhar com base nas decisões realizadas pelo algoritmo
                    algoritmo_a_estrela(
                        lambda: desenhar(janela, grade, LINHAS, lado),
                        grade,
                        inicio,
                        final,
                    )

                # se o usuario apertar l ("limpar"), o programa se reinicializa
                if evento.key == pygame.K_l:
                    inicio = None
                    final = None
                    grade = construir_grade(LINHAS, lado)
    pygame.quit()


# rodando o programa (loop principal)
if __name__ == "__main__":
    main(JANELA, LADO)

