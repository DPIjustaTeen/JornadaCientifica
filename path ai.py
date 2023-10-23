import pygame
import random
import heapq
import time
import pygame.font
import csv

pygame.font.init()
FONT = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
# Inicialização do Pygame
pygame.init()
window_size = 500
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Labirinto Aleatório (Busca em Profundidade)")

escala = 1



# Tamanho da célula do labirinto
cell_size = 25 * escala
running = True
regenerate_requested = False
waiting = False
slow_requested = False
slow = 10
battle_mode = False  # Variable for battle mode
display_active = False
elapsed_time = 0
start_time = 0
battle_time = 60000
completion_counter = 0




def display_timer(seconds):
    timer_text = f"Tempo: {seconds} segundos"
    text_surface = FONT.render(timer_text, True, black, white)
    text_rect = text_surface.get_rect()
    text_rect.center = (window_size // 2, cell_size // 2)
    window.blit(text_surface, text_rect)

def display_completion_counter(completions):
    if completions != 0:
        timer_text = f"Labirintos completos: {completions}"
        text_surface = FONT.render(timer_text, True, black, white)
        text_rect = text_surface.get_rect()
        text_rect.center = (window_size // 2, window_size - cell_size // 2)
        window.blit(text_surface, text_rect)
def update_timer():
    global current_time
    global elapsed_time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time)
    display_timer(int(elapsed_time / 1000))
    pygame.display.flip()

def update_completion_counter(battle_mode_true):
    global  completion_counter
    if battle_mode_true:
        completion_counter += 1

#def battle_time(within):
#    global regenerate_requested
#    global waiting
#    global battle_mode
#    regenerate_requested = False
#    waiting = False
#    battle_mode = True
#    return

def battle_within_time(within):
    global regenerate_requested
    global waiting
    global battle_mode
    global completion_counter
    regenerate_requested = within
    waiting = not within
    battle_mode = within
    #if within:
    #    completion_counter += 1

    return

def draw_labyrinth():
    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 1:
                # Ajustar as coordenadas x multiplicando por cell_size, adicionando o deslocamento horizontal e centralizando verticalmente
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset
                pygame.draw.rect(window, white, (x, y, cell_size, cell_size))
            else:
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset
                pygame.draw.rect(window, black, (x, y, cell_size, cell_size)) # Pintar as áreas não visitadas
            pygame.draw.rect(window, green, (exitPosx, exitPosy, cell_size, cell_size))

def show_path():
    for pos in Celulas_visitadas:
        pygame.draw.rect(window, (0, 0, 255), (pos[1] * cell_size + horizontal_offset, pos[0] * cell_size + vertical_offset, cell_size, cell_size))
        time.sleep(velAlgoritimo*2)
        update_timer()
        display_completion_counter(completion_counter)
    if path:
        for pos in path:
            pygame.draw.rect(window, (0, 255, 0), (pos[1] * cell_size + horizontal_offset, pos[0] * cell_size + vertical_offset, cell_size, cell_size))
            time.sleep(0.01)
            update_timer()
    if battle_mode:
        update_completion_counter(True)

def key_pressed(p_slow,p_regenerate_requested,p_battle_mode):
    global slow
    global regenerate_requested
    global battle_mode
    slow = p_slow
    regenerate_requested = p_regenerate_requested
    battle_mode = p_battle_mode

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A*

#Celulas_visitadas_2 = set()
def astar(start, goal, matrix):
    open_list = []
    global Celulas_visitadas
    #Celulas_visitadas = set()
    Celulas_visitadas = []
    heapq.heappush(open_list, (0, start))
    came_from = {}

    g_score = {(row, col): float('inf') for row in range(maze_rows) for col in range(maze_cols)}
    g_score[start] = 0

    f_score = {(row, col): float('inf') for row in range(maze_rows) for col in range(maze_cols)}
    f_score[start] = heuristic(start, goal)

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path

        #Celulas_visitadas.add(current)
        Celulas_visitadas.append(current)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor = current[0] + dx, current[1] + dy

            if neighbor[0] < 0 or neighbor[0] >= maze_rows or neighbor[1] < 0 or neighbor[1] >= maze_cols:
                continue

            if matrix[neighbor[0]][neighbor[1]] == 0:
                continue

            if neighbor in Celulas_visitadas:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if neighbor not in [item[1] for item in open_list]:
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None

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

# Cores
green = (0, 200, 0)
black = (0, 0, 0)
white = (255, 255, 255)
rngcolor = (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))

# Centralizar o labirinto na tela
start_row = (maze_rows-2)
start_col = (1)

# Função para criar uma matriz vazia
def create_empty_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

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

# Variáveis para o A*
start = (start_row, start_col)
goal = (exit_row, exit_col)

def regenerate_maze_and_path():
    # Create a new empty maze and regenerate it
    new_maze = create_empty_matrix(maze_rows, maze_cols)
    generate_maze_dfs(new_maze, start_row, start_col)

    # Find a new exit position
    new_exit_row = 0
    new_exit_col = maze_cols - 2
    new_maze[new_exit_row][new_exit_col] = 1

    # Regenerate the A* path using the new maze
    new_start = (start_row, start_col)
    new_goal = (new_exit_row, new_exit_col)
    new_path = astar(new_start, new_goal, new_maze)

    return new_maze, new_path, new_exit_row, new_exit_col

# Initial generation of the maze and path
maze, path, exit_row, exit_col = regenerate_maze_and_path()


while running:

    if battle_mode:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time)
        if elapsed_time >= battle_time:
            battle_within_time(False)
            completion_counter += 1
        else:
            battle_within_time(True)
        pygame.display.flip()


    velAlgoritimo = 0.1 / slow

    if regenerate_requested:
        #Regenerate the maze and path
        maze, path, exit_row, exit_col = regenerate_maze_and_path()
        regenerate_requested = False  # Reset the flag



    #Desenha novo labirinto vazio
    if not waiting:
        window.fill(white)
        draw_labyrinth()
        waiting = True
        # Executar o algoritmo A* para encontrar o caminho
        path = astar(start, goal, maze)
        path.reverse()
        #Exibir resolução
        show_path()

    #desenhar saída
    pygame.display.flip()

    #waiting = True
    while waiting and not battle_mode:

        for event in pygame.event.get():

            if event.type == pygame.KEYUP:

                start_time = pygame.time.get_ticks()
                waiting = False
                match event.key:

                    case  pygame.K_SPACE:
                        key_pressed(slow, True, False)
                        break

                    case pygame.K_1:
                        key_pressed(1, False, False)
                        break

                    case pygame.K_2:
                        key_pressed(2, False, False)
                        break

                    case pygame.K_5:
                        key_pressed(5,False,False)
                        break

                    case pygame.K_b:
                        display_active = True
                        key_pressed(3,False,True)
                        completion_counter = 0
                        break

                    case _:
                        key_pressed(10, False, False)
                        break

            break

    #Fechar jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    clock.tick(45)

# Encerrar o Pygame

pygame.quit()