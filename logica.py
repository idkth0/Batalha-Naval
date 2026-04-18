import numpy as np
import random

class Tabuleiro:
    def __init__(self, tamanho=10):
        """
        Inicializa um tabuleiro de jogo com o tamanho especificado.

        Args:
            tamanho (int): O tamanho do tabuleiro, padrão é 10.
        """
        self.tamanho = tamanho
        self.tabuleiro = np.zeros((tamanho, tamanho), dtype=int)

    def posicionar_navio(self, tamanho, linha, coluna, orientacao):
        """
        Posiciona um navio no tabuleiro.

        Args:
            tamanho (int): O tamanho do navio.
            linha (int): A linha inicial para posicionar o navio.
            coluna (int): A coluna inicial para posicionar o navio.
            orientacao (str): A orientação do navio, "horizontal" ou "vertical".

        Returns:
            bool: True se o navio foi posicionado com sucesso, False caso contrário.
        """
        if orientacao == "horizontal" and coluna + tamanho <= self.tamanho:
            if np.all(self.tabuleiro[linha, coluna:coluna + tamanho] == 0):
                self.tabuleiro[linha, coluna:coluna + tamanho] = 1
                return True
        elif orientacao == "vertical" and linha + tamanho <= self.tamanho:
            if np.all(self.tabuleiro[linha:linha + tamanho, coluna] == 0):
                self.tabuleiro[linha:linha + tamanho, coluna] = 1
                return True
        return False

    def atacar(self, linha, coluna):
        """
        Realiza um ataque em uma posição do tabuleiro.

        Args:
            linha (int): A linha do ataque.
            coluna (int): A coluna do ataque.

        Returns:
            bool: True se um navio foi acertado, False se foi água, None se a posição já foi atacada.
        """
        if self.tabuleiro[linha, coluna] == 1:
            self.tabuleiro[linha, coluna] = -1  
            return True
        elif self.tabuleiro[linha, coluna] == 0:
            self.tabuleiro[linha, coluna] = -2  
            return False
        return None  
    
    def todos_navios_destruidos(self):
        """
        Verifica se todos os navios foram destruídos.

        Returns:
            bool: True se todos os navios foram destruídos, False caso contrário.
        """
        return np.all(self.tabuleiro[self.tabuleiro == 1] == -1)

class JogoBatalhaNaval:
    def __init__(self):
        """
        Inicializa o jogo de Batalha Naval, configurando tabuleiros e navios.
        """
        self.tamanho = 10
        self.navios = {"porta_avioes": 5, "encouracado": 4, "cruzador": 3, "submarino": 3, "destruidor": 2}
        self.tabuleiro_jogador = Tabuleiro(self.tamanho)
        self.tabuleiro_bot = Tabuleiro(self.tamanho)
        self.acertos_bot = []
        self.fim_de_jogo = False

    def posicionar_navios_jogador(self, posicoes):
        """
        Posiciona os navios do jogador no tabuleiro.

        Args:
            posicoes (dict): Um dicionário com as posições dos navios.

        Returns:
            bool: True se todos os navios foram posicionados com sucesso, False caso contrário.
        """
        for navio, (linha, coluna, orientacao) in posicoes.items():
            if not self.tabuleiro_jogador.posicionar_navio(self.navios[navio], linha, coluna, orientacao):
                return False
        return True

    def posicionar_navios_bot(self):
        """
        Posiciona os navios do bot no tabuleiro de forma aleatória.
        """
        for tamanho in self.navios.values():
            while True:
                orientacao = random.choice(["horizontal", "vertical"])
                linha = random.randint(0, self.tamanho - (tamanho if orientacao == "vertical" else 1))
                coluna = random.randint(0, self.tamanho - (tamanho if orientacao == "horizontal" else 1))
                if self.tabuleiro_bot.posicionar_navio(tamanho, linha, coluna, orientacao):
                    break

    def ataque_aleatorio(self, tabuleiro):
        """
        Realiza um ataque aleatório no tabuleiro.

        Args:
            tabuleiro (Tabuleiro): O tabuleiro a ser atacado.

        Returns:
            tuple: As coordenadas do ataque (linha, coluna).
        """
        while True:
            linha = random.randint(0, self.tamanho - 1)
            coluna = random.randint(0, self.tamanho - 1)
            if tabuleiro.tabuleiro[linha, coluna] >= 0:
                return linha, coluna

    def ataque_inteligente(self, tabuleiro):
        """
        Realiza um ataque inteligente no tabuleiro com base em acertos anteriores.

        Args:
            tabuleiro (Tabuleiro): O tabuleiro a ser atacado.

        Returns:
            tuple: As coordenadas do ataque (linha, coluna).
        """
        if self.acertos_bot:
            ultima_linha, ultima_coluna = self.acertos_bot[-1]
            direcoes = [
                (ultima_linha - 1, ultima_coluna), (ultima_linha + 1, ultima_coluna),
                (ultima_linha, ultima_coluna - 1), (ultima_linha, ultima_coluna + 1)
            ]
            random.shuffle(direcoes)
            for linha, coluna in direcoes:
                if 0 <= linha < self.tamanho and 0 <= coluna < self.tamanho and tabuleiro.tabuleiro[linha, coluna] >= 0:
                    return linha, coluna
        return self.ataque_aleatorio(tabuleiro)

    def jogar(self):
        """
        Inicia o jogo de Batalha Naval, permitindo que o jogador e o bot ataquem alternadamente
        até que todos os navios de um dos jogadores sejam destruídos.
        """
        # Posições dos navios do jogador pré-definidas para simplificação
        posicoes_navios_jogador = {
            "porta_avioes": (0, 0, "horizontal"), "encouracado": (2, 2, "vertical"),
            "cruzador": (4, 4, "horizontal"), "submarino": (6, 6, "vertical"), "destruidor": (8, 8, "horizontal")
        }

        # Posiciona os navios do jogador no tabuleiro
        if not self.posicionar_navios_jogador(posicoes_navios_jogador):
            print("Erro ao posicionar navios do jogador.")
            return

        # Posiciona os navios do bot no tabuleiro de forma aleatória
        self.posicionar_navios_bot()

        # Loop principal do jogo
        while not self.fim_de_jogo:
            # Turno do jogador
            linha = int(input("Digite a linha para atacar (0-9): "))
            coluna = int(input("Digite a coluna para atacar (0-9): "))
            resultado = self.tabuleiro_bot.atacar(linha, coluna)
            print("Você acertou!" if resultado else "Você errou!" if resultado is False else "Você já atacou essa posição antes.")

            # Verifica se todos os navios do bot foram destruídos
            if self.tabuleiro_bot.todos_navios_destruidos():
                print("Você venceu!")
                self.fim_de_jogo = True
                continue

            # Turno do bot
            if self.acertos_bot and any(self.tabuleiro_jogador.tabuleiro[linha, coluna] == -1 for linha, coluna in self.acertos_bot):
                linha, coluna = self.ataque_inteligente(self.tabuleiro_jogador)
            else:
                linha, coluna = self.ataque_aleatorio(self.tabuleiro_jogador)

            resultado = self.tabuleiro_jogador.atacar(linha, coluna)
            print("A máquina acertou!" if resultado else "A máquina errou!")

            # Adiciona o acerto aos acertos do bot
            if resultado:
                self.acertos_bot.append((linha, coluna))

            # Verifica se todos os navios do jogador foram destruídos
            if self.tabuleiro_jogador.todos_navios_destruidos():
                print("A máquina venceu!")
                self.fim_de_jogo = True