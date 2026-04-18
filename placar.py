class Placar:
    def __init__(self):
        """
        Inicializa um objeto Placar com contadores de vitórias para o jogador e o bot.
        """
        self.vitorias_jogador = 0
        self.vitorias_bot = 0

    def atualizar_placar(self, jogador_ganhou):
        """
        Atualiza o placar com base no resultado do jogo.

        Args:
            jogador_ganhou (bool): True se o jogador ganhou, False se o bot ganhou.
        """
        if jogador_ganhou:
            self.vitorias_jogador += 1
        else:
            self.vitorias_bot += 1

    def mostrar_placar(self):
        """
        Retorna o placar atual.

        Returns:
            str: Uma string formatada mostrando o número de vitórias do jogador e do bot.
        """
        return f"Jogador: {self.vitorias_jogador} - R2d2: {self.vitorias_bot}"