import tkinter as tk
import tkinter.messagebox as messagebox
from logica import JogoBatalhaNaval
from placar import Placar
import numpy as np

class InterfaceJogo:
    def __init__(self, root):
        """
        Inicializa a interface do jogo Batalha Naval.

        Args:
            root (tk.Tk): A janela principal do Tkinter.
        """
        self.root = root
        self.root.title("Batalha Naval")
        self.jogo = JogoBatalhaNaval()
        self.placar = Placar()

        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack()

        self.board_size = 10
        self.ships = [5, 4, 3, 3, 2]
        self.selected_cells = []
        self.current_ship_index = 0
        self.jogador_turno = True

        self.criar_interface_posicionamento()

    def criar_interface_posicionamento(self):
        """
        Cria a interface de posicionamento dos navios.
        """
        self.limpar_frame()

        tk.Label(self.frame_principal, text="Posicione seus navios").pack()

        self.frame_tabuleiro_jogador = tk.Frame(self.frame_principal)
        self.frame_tabuleiro_jogador.pack()
        self.criar_tabuleiro_interface(self.frame_tabuleiro_jogador, self.jogo.tabuleiro_jogador.tabuleiro, False, self.selecionar_celula)

        self.update_status()

    def criar_tabuleiro_interface(self, frame, tabuleiro, is_bot, command):
        """
        Cria a interface gráfica para o tabuleiro.

        Args:
            frame (tk.Frame): O frame onde o tabuleiro será criado.
            tabuleiro (np.ndarray): O tabuleiro do jogo.
            is_bot (bool): Se o tabuleiro pertence ao bot.
            command (function): A função a ser chamada ao clicar em uma célula.
        """
        self.buttons = []
        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                button = tk.Button(frame, text="~", width=3, height=2,
                                   command=lambda x=i, y=j: command(x, y))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

        self.status_label = tk.Label(self.frame_principal, text="", font=("Arial", 14))
        self.status_label.pack()

    def selecionar_celula(self, i, j):
        """
        Seleciona uma célula no tabuleiro para posicionar um navio.

        Args:
            i (int): A linha da célula.
            j (int): A coluna da célula.
        """
        if self.jogo.tabuleiro_jogador.tabuleiro[i, j] == 0:
            self.jogo.tabuleiro_jogador.tabuleiro[i, j] = 1
            self.selected_cells.append((i, j))
            self.buttons[i][j].config(text="S", bg="blue")

            if len(self.selected_cells) == self.ships[self.current_ship_index]:
                if self.validar_celula():
                    self.local_navio()
                    self.current_ship_index += 1
                    if self.current_ship_index < len(self.ships):
                        self.update_status()
                    else:
                        messagebox.showinfo("Batalha Naval", "Todos os navios foram posicionados!")
                        self.confirmar_posicionamento()
                else:
                    messagebox.showerror("Erro", "Posição inválida para o navio. Tente novamente.")
                    self.limpar_selecao()
        else:
            messagebox.showwarning("Atenção", "Essa célula já foi selecionada.")

    def validar_celula(self):
        """
        Valida se as células selecionadas formam uma posição válida para o navio.

        Returns:
            bool: True se a posição for válida, False caso contrário.
        """
        if len(self.selected_cells) == 1:
            return True

        self.selected_cells.sort()
        is_horizontal = all(i == self.selected_cells[0][0] for i, j in self.selected_cells)
        is_vertical = all(j == self.selected_cells[0][1] for i, j in self.selected_cells)

        if is_horizontal:
            return all(j == self.selected_cells[0][1] + idx for idx, (i, j) in enumerate(self.selected_cells))
        elif is_vertical:
            return all(i == self.selected_cells[0][0] + idx for idx, (i, j) in enumerate(self.selected_cells))

        return False

    def local_navio(self):
        """
        Posiciona o navio nas células selecionadas.
        """
        for i, j in self.selected_cells:
            self.buttons[i][j].config(bg="gray")
        self.selected_cells = []

    def limpar_selecao(self):
        """
        Limpa a seleção atual de células.
        """
        for i, j in self.selected_cells:
            self.jogo.tabuleiro_jogador.tabuleiro[i, j] = 0
            self.buttons[i][j].config(text="~", bg="SystemButtonFace")
        self.selected_cells = []

    def update_status(self):
        """
        Atualiza a mensagem de status na interface.
        """
        self.status_label.config(text=f"Posicione o navio de tamanho {self.ships[self.current_ship_index]}")

    def confirmar_posicionamento(self):
        """
        Confirma o posicionamento dos navios e inicia o jogo.
        """
        self.jogo.posicionar_navios_bot()
        self.criar_interface_jogo()

    def criar_interface_jogo(self):
        """
        Cria a interface do jogo após o posicionamento dos navios.
        """
        self.limpar_frame()

        self.tabuleiro_jogador = self.jogo.tabuleiro_jogador.tabuleiro
        self.tabuleiro_bot = self.jogo.tabuleiro_bot.tabuleiro

        self.frame_tabuleiro_jogador = tk.Frame(self.frame_principal)
        self.frame_tabuleiro_jogador.pack(side=tk.LEFT)
        self.frame_tabuleiro_bot = tk.Frame(self.frame_principal)
        self.frame_tabuleiro_bot.pack(side=tk.RIGHT)

        self.criar_tabuleiro_interface(self.frame_tabuleiro_jogador, self.tabuleiro_jogador, False, self.acao_ataque_jogador)
        self.criar_tabuleiro_interface(self.frame_tabuleiro_bot, self.tabuleiro_bot, True, self.acao_ataque_jogador)

        self.label_turno = tk.Label(self.frame_principal, text="Turno do Jogador")
        self.label_turno.pack()

        self.placar_label = tk.Label(self.frame_principal, text=self.placar.mostrar_placar(), font=("Arial", 14))
        self.placar_label.pack()

        tk.Button(self.frame_principal, text="Jogar Novamente", command=self.reiniciar_jogo).pack()

        self.atualizar_tabuleiro(self.frame_tabuleiro_jogador, self.tabuleiro_jogador)
        self.atualizar_tabuleiro(self.frame_tabuleiro_bot, self.tabuleiro_bot, ocultar=True)

    def atualizar_tabuleiro(self, frame, tabuleiro, ocultar=False):
        """
        Atualiza a interface do tabuleiro com as informações atuais do jogo.

        Args:
            frame (tk.Frame): O frame do tabuleiro.
            tabuleiro (np.ndarray): O tabuleiro do jogo.
            ocultar (bool): Se as células devem ser ocultadas (para o tabuleiro do bot).
        """
        for i in range(tabuleiro.shape[0]):
            for j in range(tabuleiro.shape[1]):
                btn = frame.grid_slaves(row=i, column=j)[0]
                if tabuleiro[i, j] == 1 and not ocultar:
                    btn.config(bg="black")
                elif tabuleiro[i, j] == -1:
                    btn.config(bg="red", text="X")
                elif tabuleiro[i, j] == -2:
                    btn.config(bg="black", text="O")
                else:
                    btn.config(bg="blue")

    def acao_ataque_jogador(self, linha, coluna):
        """
        Realiza a ação de ataque do jogador.

        Args:
            linha (int): A linha da célula atacada.
            coluna (int): A coluna da célula atacada.
        """
        if self.jogo.fim_de_jogo or not self.jogador_turno:
            return

        resultado = self.jogo.tabuleiro_bot.atacar(linha, coluna)
        if resultado is None:
            messagebox.showerror("Erro", "Você já atacou essa posição antes.")
        elif resultado:
            self.frame_tabuleiro_bot.grid_slaves(row=linha, column=coluna)[0].config(bg="green", text="X")
        else:
            self.frame_tabuleiro_bot.grid_slaves(row=linha, column=coluna)[0].config(bg="red", text="O")

        if self.jogo.tabuleiro_bot.todos_navios_destruidos():
            messagebox.showinfo("Fim de Jogo", "Você venceu!")
            self.jogo.fim_de_jogo = True
            self.placar.atualizar_placar(True)
            self.placar_label.config(text=self.placar.mostrar_placar())
            return

        self.jogador_turno = False
        self.label_turno.config(text="Turno do R2d2")
        self.root.after(1000, self.ataque_bot)

    def ataque_bot(self):
        """
        Realiza a ação de ataque do bot.
        """
        if self.jogo.fim_de_jogo:
            return

        linha, coluna = self.jogo.ataque_inteligente(self.jogo.tabuleiro_jogador)
        resultado = self.jogo.tabuleiro_jogador.atacar(linha, coluna)
        if resultado is None:
            self.ataque_bot()
        elif resultado:
            self.frame_tabuleiro_jogador.grid_slaves(row=linha, column=coluna)[0].config(bg="green", text="X")
            self.jogo.acertos_bot.append((linha, coluna))
        else:
            self.frame_tabuleiro_jogador.grid_slaves(row=linha, column=coluna)[0].config(bg="red", text="O")

        if self.jogo.tabuleiro_jogador.todos_navios_destruidos():
            messagebox.showinfo("Fim de Jogo", "R2d2 venceu!")
            self.jogo.fim_de_jogo = True
            self.placar.atualizar_placar(False)
            self.placar_label.config(text=self.placar.mostrar_placar())
            return

        self.jogador_turno = True
        self.label_turno.config(text="Turno do Jogador")

    def limpar_frame(self):
        """
        Limpa todos os widgets do frame principal.
        """
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def reiniciar_jogo(self):
        """
        Reinicia o jogo, resetando todas as variáveis e interfaces.
        """
        self.jogo = JogoBatalhaNaval()
        self.current_ship_index = 0
        self.selected_cells = []
        self.jogador_turno = True
        self.criar_interface_posicionamento()

if __name__ == "__main__":
    root = tk.Tk()
    interface_jogo = InterfaceJogo(root)
    root.mainloop()