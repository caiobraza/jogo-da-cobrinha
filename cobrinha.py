# --- 1. IMPORTAÇÃO DAS BIBLIOTECAS ---
import pygame   # Importa a biblioteca principal do Pygame para criar jogos em 2D
import random   # Importa funções para sortear números (usado para posicionar a comida aleatoriamente)

# ==========================================
# 2. CONSTANTES E CONFIGURAÇÕES DO JOGO
# ==========================================
LARGURA, ALTURA = 600, 400  # Define o tamanho da janela do jogo (600 pixels de largura por 400 de altura)
TAMANHO_BLOCO = 20          # Tamanho em pixels de cada quadrado da grade (corpo da cobra e comida)
FPS = 10                    # Velocidade do jogo (quantas vezes a tela atualiza por segundo)

# Paleta de Cores Cyberpunk (Neon & Dark) - Cores em formato RGB (Vermelho, Verde, Azul)
COR_FUNDO = (15, 15, 25)          # Azul escuro profundo (quase preto para o fundo da tela)
COR_GRAMA = (25, 25, 40)          # Tom ligeiramente mais claro para criar o padrão xadrez no fundo
COR_COBRA = (0, 255, 200)         # Ciano neon vibrante para colorir a cobra
COR_COMIDA = (255, 0, 127)        # Rosa choque / Magenta neon para colorir a comida
COR_TEXTO = (255, 255, 0)         # Amarelo neon para destacar o placar de pontos

# ==========================================
# 3. FUNÇÕES AUXILIARES
# ==========================================
def criar_comida():
    """Gera uma nova posição aleatória para a comida na tela."""
    x = random.randrange(0, LARGURA, TAMANHO_BLOCO)         # Sorteia uma posição horizontal alinhada à grade
    y = random.randrange(40, ALTURA, TAMANHO_BLOCO)        # Sorteia uma posição vertical (abaixo do placar)
    return pygame.Rect(x, y, TAMANHO_BLOCO, TAMANHO_BLOCO) # Retorna um retângulo representando a comida

# ==========================================
# 4. FUNÇÃO PRINCIPAL DO JOGO
# ==========================================
def main():
    # Inicialização do Pygame e criação da janela
    pygame.init()                                  # Inicializa todos os módulos do Pygame
    tela = pygame.display.set_mode((LARGURA, ALTURA)) # Cria a janela do jogo com as dimensões definidas
    pygame.display.set_caption("Cyberpunk Snake")  # Define o título que aparece na barra superior da janela
    relogio = pygame.time.Clock()                  # Cria um relógio interno para controlar a taxa de quadros por segundo (FPS)
    fonte = pygame.font.Font(None, 40)             # Define a fonte e o tamanho do texto do placar

    # Estado inicial da cobra e pontuação
    # Cria os 3 primeiros blocos da cobra alinhados na horizontal
    inicio = [pygame.Rect(x, 200, TAMANHO_BLOCO, TAMANHO_BLOCO) for x in (80, 60, 40)]
    cobra = inicio.copy()                          # Copia a lista inicial para a variável da cobra ativa
    direcao = (1, 0)                               # Define que a cobra começa andando para a direita (eixo X positivo)
    comida = criar_comida()                        # Gera a primeira comida no mapa
    pontos = 0                                     # Zera a pontuação inicial do jogador

    # Mapeamento de teclas do teclado para direções (vetores X e Y)
    setas = {
        pygame.K_LEFT: (-1, 0),    # Seta para a esquerda (anda para trás no eixo X)
        pygame.K_RIGHT: (1, 0),    # Seta para a direita (anda para frente no eixo X)
        pygame.K_UP: (0, -1),      # Seta para cima (anda para cima no eixo Y)
        pygame.K_DOWN: (0, 1),     # Seta para baixo (anda para baixo no eixo Y)
    }

    rodando = True                  # Variável de controle para manter o jogo aberto
    while rodando:                  # Loop principal do jogo (roda a cada frame)
        
        # --- A. TRATAMENTO DE EVENTOS ---
        for evento in pygame.event.get():          # Lê todos os eventos que o usuário faz (teclado, mouse, fechar janela)
            if evento.type == pygame.QUIT:         # Se o usuário clicar no 'X' da janela
                rodando = False                    # Encerra o loop e fecha o jogo
            if evento.type == pygame.KEYDOWN:      # Se o usuário apertar alguma tecla do teclado
                nova = setas.get(evento.key, direcao) # Verifica se a tecla apertada é uma das setas válidas
                # Impede que a cobra dê meia-volta imediata sobre o próprio corpo (ex: ir direto da direita para a esquerda)
                if nova != (-direcao[0], -direcao[1]):
                    direcao = nova                 # Atualiza a direção da cobra

        # --- B. LÓGICA DO JOGO ---
        dx, dy = direcao                           # Separa a direção atual em deslocamento X e Y
        # Cria uma nova cabeça para a cobra avançando um bloco na direção atual
        cabeca = cobra[0].move(dx * TAMANHO_BLOCO, dy * TAMANHO_BLOCO) 
        
        # Verifica se a cobra bateu na parede (saiu da tela) ou colidiu com o próprio corpo
        fora = not tela.get_rect().contains(cabeca)
        if fora or cabeca.collidelist(cobra) >= 0:
            cobra = inicio.copy()                  # Reseta o tamanho e posição inicial da cobra
            direcao = (1, 0)                       # Reseta a direção para a direita
            pontos = 0                             # Zera os pontos
            continue                               # Reinicia o ciclo do loop atual

        cobra.insert(0, cabeca)                    # Adiciona a nova cabeça no início da lista da cobra

        # Verifica se a cabeça da cobra encostou na comida
        if cabeca == comida:
            pontos += 1                            # Aumenta 1 ponto na placar
            comida = criar_comida()                # Gera uma nova comida em outro lugar
        else:
            cobra.pop()                            # Remove o último bloco da cauda (faz a cobra andar sem crescer infinitamente)

        # --- C. RENDERIZAÇÃO (DESENHO NA TELA) ---
        tela.fill(COR_FUNDO)                       # Pinta o fundo inteiro da tela com a cor escuro cyberpunk
        
        # Desenhando o grid de fundo (padrão xadrejado discreto)
        for x in range(0, LARGURA, TAMANHO_BLOCO):
            for y in range(x % 40, ALTURA, 40):
                pygame.draw.rect(tela, COR_GRAMA, (x, y, TAMANHO_BLOCO, TAMANHO_BLOCO))

        # Placar de pontos (renderiza o texto e desenha na tela em amarelo neon)
        placar = fonte.render(f"PONTOS: {pontos}", 1, COR_TEXTO)
        tela.blit(placar, (10, 10))

        # Desenhando a cobra (com blocos levemente arredondados nos cantos para dar efeito futurista)
        for parte in cobra:
            pygame.draw.rect(tela, COR_COBRA, parte, 0, 4)

        # Desenhando a comida (em formato de círculo rosa neon bem brilhante)
        pygame.draw.circle(tela, COR_COMIDA, comida.center, 9)

        pygame.display.flip()                      # Atualiza tudo o que foi desenhado na tela para o usuário ver
        relogio.tick(FPS)                          # Aguarda o tempo necessário para manter a velocidade constante (FPS)

    pygame.quit()                                  # Fecha os módulos do Pygame ao sair do loop

if __name__ == "__main__":
    main()                                         # Executa a função principal quando o arquivo é rodado diretamente