import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# relogio
clock = pygame.time.Clock()

# Numero de compleções
numero_complecoes = 0

# Configurações da janela
window_size = 500
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Labirinto Aleatório (Busca em Profundidade)")

# Tamanho da célula do labirinto
cell_size = 25

#Quantidade de linhas e colunas
maze_rows = int((window_size-(4* cell_size)) /cell_size)


if maze_rows % 2 == 0:
    maze_rows += 1

maze_cols = maze_rows

# Calcular o deslocamento horizontal para centralizar o labirinto
horizontal_offset = (window_size - (maze_rows * cell_size)) // 2
# Calcular o deslocamento vertical para centralizar o labirinto
vertical_offset = (window_size - (maze_rows * cell_size)) // 2

# Tamanho total do quadrado do labirinto
maze_square_size = maze_rows*cell_size

divEscalaPlayer = 2
cuboTamX = cell_size
cuboTamY = cell_size
cuboX = (window_size - cuboTamX)//2


# tempo por tentativa
# 60 segundos = 1 minuto
loop_duration = 60
start_time = time.time()

# Cores
green = (0, 200, 0)
black = (0, 0, 0)
white = (255, 255, 255)
FONT = pygame.font.Font(None, 36)
rngcolor = (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))

cubo_image_original = pygame.image.load("images/cubo.png")
cubo_image_cima = pygame.image.load("images/cima.png")
cubo_image_baixo = pygame.image.load("images/baixo.png")
cubo_image_esquerda = pygame.image.load("images/esquerda.png")
cubo_image_direita = pygame.image.load("images/direita.png")
novo_tamanho = (cubo_image_direita.get_width(), cubo_image_direita.get_height())

cubo_image = {'original': cubo_image_original, 'cima': cubo_image_cima, 'baixo':cubo_image_baixo, 'esquerda':cubo_image_esquerda, 'direita':cubo_image_direita}

# Ajustar as dimensões do labirinto para caber no quadrado
#maze_rows = maze_square_size // cell_size
#maze_cols = maze_rows

# Centralizar o labirinto na tela
start_row = (maze_rows-2) // 2
start_col = (maze_cols-2) // 2



# Função para criar uma matriz vazia
def create_empty_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

# Definir timer
def display_timer(seconds):
    timer_text = f"Tempo: {seconds} segundos"
    text_surface = FONT.render(timer_text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (window_size // 2, cell_size // 2)
    window.blit(text_surface, text_rect)

def display_numero_complecoes(numero_complecoes):
    complecoes_text = f"Vitórias: {numero_complecoes} "
    text_surface = FONT.render(complecoes_text, True, black)
    text_rect = text_surface.get_rect()
    text_rect.center = (window_size // 2, window_size - (cell_size // 2))
    window.blit(text_surface, text_rect)

# Função para gerar o labirinto usando1busca em profundidade
def generate_maze_dfs(matrix, row, col):
    matrix[row][col] = 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        new_row, new_col = row + 2 * dr, col + 2 * dc
        if 0 <= new_row < maze_rows and 0 <= new_col < maze_cols and matrix[new_row][new_col] == 0:
            matrix[row + dr][col + dc] = 1
            generate_maze_dfs(matrix, new_row, new_col)

# Criar uma matriz vazia para o labirinto
maze = create_empty_matrix(maze_rows, maze_cols)

# Iniciar a geração do labirinto a partir do centro
generate_maze_dfs(maze, start_row, start_col)

# Definir a posição da saída na última coluna e na última linha
exit_row = 0
exit_col = maze_cols - 2
maze[exit_row][exit_col] = 1

exitPosx = exit_col * cell_size + horizontal_offset
exitPosy = exit_row * cell_size + vertical_offset #- 12

#Posição inicial do cubo
element_row = maze_rows - 2
element_col = maze_cols - (maze_cols-1)

element_global_x = element_col * cell_size + horizontal_offset
element_global_y = element_row * cell_size + vertical_offset #- 12

#escala da imagem
cuboX = element_global_x
cuboY = element_global_y
velCubo = 5
cubo_image_original = pygame.image.load("images/cubo.png")
novo_tamanho = (cubo_image_original.get_width() // divEscalaPlayer, cubo_image_original.get_height() // divEscalaPlayer)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    elapsed_time = current_time - start_time


    if elapsed_time >= loop_duration:
        pygame.quit()


    # Movimentação do cubo
    keys = pygame.key.get_pressed()
    new_cubo_image = pygame.transform.scale(cubo_image['original'], novo_tamanho)

    if keys[pygame.K_a]:
        new_cubo_image = pygame.transform.scale(cubo_image['esquerda'], novo_tamanho)
        if (cuboY-horizontal_offset) % cell_size == 0:
            new_cuboX = cuboX - velCubo
            new_row = int((cuboY - vertical_offset + cuboTamY / 2) / cell_size)
            new_col = int((new_cuboX - horizontal_offset) / cell_size)

            if maze[new_row][new_col] == 1:
                cuboX = new_cuboX

    if keys[pygame.K_d]:
        new_cubo_image = pygame.transform.scale(cubo_image['direita'], novo_tamanho)
        if (cuboY-horizontal_offset) % cell_size == 0:
            new_cuboX = cuboX + velCubo
            new_row = int((cuboY - vertical_offset + cuboTamY / 2) / cell_size)
            new_col = int((new_cuboX - horizontal_offset + cuboTamX - 1) / cell_size)

            if maze[new_row][new_col] == 1:
                cuboX = new_cuboX

    if keys[pygame.K_w]:
        new_cubo_image = pygame.transform.scale(cubo_image['cima'], novo_tamanho)
        if (cuboX-vertical_offset) % cell_size == 0:
            new_cuboY = cuboY - velCubo
            new_row = int((new_cuboY - vertical_offset ) / cell_size)
            new_col = int((cuboX - horizontal_offset + cuboTamX / 2) / cell_size)

            if maze[new_row][new_col] == 1:
                cuboY = new_cuboY

    if keys[pygame.K_s]:
        new_cubo_image = pygame.transform.scale(cubo_image['baixo'], novo_tamanho)
        if (cuboX-vertical_offset) % cell_size == 0:
            new_cuboY = cuboY + velCubo
            new_row = int((new_cuboY - vertical_offset + cuboTamY-1) / cell_size)
            new_col = int((cuboX - horizontal_offset + cuboTamX / 2) / cell_size)

            if maze[new_row][new_col] == 1:
                cuboY = new_cuboY


    cuboX = max(0, min(cuboX, window_size - cuboTamX))
    cuboY = max(0, min(cuboY, window_size - cuboTamY))

    if cuboX == exitPosx and cuboY == exitPosy:
        maze = create_empty_matrix(maze_rows, maze_cols)
        generate_maze_dfs(maze, start_row, start_col)
        exit_row = 0
        exit_col = maze_cols - 2
        maze[exit_row][exit_col] = 1
        cuboX = element_global_x
        cuboY = element_global_y
        rngcolor = (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))
        numero_complecoes += 1

    window.fill(white)

    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 1:
                # Ajustar as coordenadas x multiplicando por cell_size, adicionando o deslocamento horizontal e centralizando verticalmente
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset

                # Centralizar verticalmente subtraindo half_cell_size da coordenada y
                #half_cell_size = cell_size // 2
                #y -= half_cell_size

                pygame.draw.rect(window, white, (x, y, cell_size, cell_size))
            else:
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset
                #half_cell_size = cell_size // 2
                #y -= half_cell_size
                pygame.draw.rect(window, black, (x, y, cell_size, cell_size)) # Pintar as áreas não visitadas
    #desenhar saída
    pygame.draw.rect(window, green, (exitPosx, exitPosy, cuboTamX, cuboTamY))
    #desenhar cubo
    pygame.draw.rect(window, rngcolor, (cuboX, cuboY, cuboTamX, cuboTamY))
    #desenhar spawn
    pygame.draw.rect(window, rngcolor, (element_global_x, element_global_y, cuboTamX, cuboTamY))
    window.blit(new_cubo_image, (cuboX, cuboY))

    display_timer(60 - int(elapsed_time))
    display_numero_complecoes(numero_complecoes)
    pygame.display.flip()
    clock.tick(45)


# Encerrar o Pygame
pygame.quit()