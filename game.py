import pygame
import sys
import time

pygame.init()
Window = pygame.display.set_mode((700, 700))
pygame.display.set_caption("SUDOKO SOLVER")
icon = pygame.image.load(r"C:\Users\yasmin\Downloads\IT-level3-semster1\Ai\testProject\gg.PNG")
pygame.display.set_icon(icon)

background = pygame.image.load(r"C:\Users\yasmin\Downloads\IT-level3-semster1\Ai\testProject\oo.PNG")
background = pygame.transform.scale(background, (850, 850))

ofwhite = (99, 99, 99)
black = (0, 0, 0)
button_color = (0, 0, 0)
hover_color = (54, 12, 5)
button_rect = pygame.Rect(275, 400, 150, 70)
button_font = pygame.font.Font(None, 30)
button_text = button_font.render("NEW GAME", True, (255, 255, 255))

level_buttons = {
    "easy": pygame.Rect(275, 200, 150, 70),
    "medium": pygame.Rect(275, 300, 150, 70),
    "hard": pygame.Rect(275, 400, 150, 70)
}
level_texts = {
    "easy": button_font.render("EASY", True, (255, 255, 255)),
    "medium": button_font.render("MEDIUM", True, (255, 255, 255)),
    "hard": button_font.render("HARD", True, (255, 255, 255))
}

grid_size = 9
cell_size = 50
grid_width = grid_size * cell_size
grid_height = grid_size * cell_size
start_x = (700 - grid_width) // 2
start_y = (700 - grid_height) // 2

font_path1 = r"C:\Users\yasmin\Downloads\IT-level3-semster1\Ai\testProject\BlackOpsOne-Regular.ttf"
font_1 = pygame.font.Font(font_path1, 70)
text_1 = font_1.render("SUDOKO.GAME", True, (89, 12, 5))
text_1_rect = text_1.get_rect(center=(350, 150))

font_path_2 = r"C:\Users\yasmin\Downloads\IT-level3-semster1\Ai\testProject\Pacifico-Regular.ttf"
font_2 = pygame.font.Font(font_path1, 35)
text_2 = font_2.render("ARE YOU READY!", True, (255, 255, 255))
text_2_rect = text_2.get_rect(center=(350, 335))

font = pygame.font.Font(None, 30)

errors_count = 0
max_errors = 3
start_time = None
current_level = "easy"

def reset_game(level):
    global board, locked_cells, errors_count, start_time

    if level == "hard":
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    elif level == "medium":
        board = [
            [0, 0, 0, 2, 6, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 4, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [7, 0, 3, 0, 1, 8, 0, 0, 0]
        ]
    elif level == "easy":
        board = [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ]
    locked_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]
    errors_count = 0  
    current_level = level
    start_time = time.time()  
    print("Game has been reset after game over.")

def set_difficulty(level):
    global current_level
    current_level = level
    reset_game(level)

def solveSudoko(board):
    find = findEmptyCell(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if validBoard(board, i, (row, col)):
            board[row][col] = i
            if solveSudoko(board):
                return True
            board[row][col] = 0 
    return False

def findEmptyCell(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 0:
                return (row, col)
    return None

class SelectNumber:
    def __init__(self, pygame, font):
        self.btn_w = 50
        self.btn_h = 50
        self.my_font = font
        self.color_selected = (0, 0, 0)
        self.color_normal = (54, 12, 5)
        self.buttons = []
        self.selected_number = None
        self.dragging = False
        self.dragged_number = None
        self.dragged_rect = None

        for col in range(9):
            number = col + 1
            btn_rect = pygame.Rect(
                start_x + col * self.btn_w,
                start_y + grid_height + 10,
                self.btn_w,
                self.btn_h
            )
            self.buttons.append((btn_rect, number))

        self.solve_button_rect = pygame.Rect(start_x + grid_width + 10, start_y + grid_height // 2 - 25, 80, 50)
        self.solve_button_text = font.render("Solve", True, (255, 255, 255))

    def draw(self, surface):
        for btn_rect, number in self.buttons:
            color = self.color_selected if self.selected_number == number else self.color_normal
            pygame.draw.rect(surface, color, btn_rect, width=3, border_radius=10)
            num_text = self.my_font.render(str(number), True, black)
            surface.blit(num_text, num_text.get_rect(center=btn_rect.center))

        if self.dragging and self.dragged_number is not None:
            num_text = self.my_font.render(str(self.dragged_number), True, black)
            surface.blit(num_text, self.dragged_rect)

        pygame.draw.rect(surface, button_color, self.solve_button_rect, border_radius=10)
        surface.blit(self.solve_button_text, self.solve_button_text.get_rect(center=self.solve_button_rect.center))

    def handle_click(self, pos):
        global errors_count
        if errors_count >= max_errors:
            return

        for rect, number in self.buttons:
            if rect.collidepoint(pos):
                self.selected_number = number
                self.dragging = True
                self.dragged_number = number
                self.dragged_rect = rect.copy()

        if self.solve_button_rect.collidepoint(pos):
            self.solve_button_pressed()

    def solve_button_pressed(self):
        global errors_count
        if errors_count >= max_errors:
            return
        print("Solve button pressed")
        display_message("Solving...")
        time.sleep(2)
        solveSudoko(board)
        
    def handle_drag(self, pos):
        if self.dragging and self.dragged_rect is not 0:
            self.dragged_rect.topleft = (pos[0] - self.btn_w // 2, pos[1] - self.btn_h // 2)

    def handle_release(self, pos, board, locked_cells):
        global errors_count
        if self.dragging:
            for row in range(9):
                for col in range(9):
                    cell_rect = pygame.Rect(start_x + col * cell_size, start_y + row * cell_size, cell_size, cell_size)
                    if cell_rect.collidepoint(pos):
                        if (row, col) not in locked_cells: 
                            if validBoard(board, self.dragged_number, (row, col)):
                                board[row][col] = self.dragged_number
                            else:
                                errors_count += 1
                        break  
            self.dragging = False
            self.dragged_number = None
            self.dragged_rect = None

select_number = SelectNumber(pygame, font)

def display_message(message):
    global Window
    message_text = font.render(message, True, (255, 0, 0))
    Window.fill(ofwhite)
    Window.blit(message_text, (start_x + 150, start_y + 150))
    pygame.display.update()

def draw_errors(surface, errors_count, max_errors):
    error_text = font.render(f"Errors: {errors_count}/{max_errors}", True, black)
    surface.blit(error_text, (10, 10))

    if errors_count >= max_errors:
        game_over_text = font.render(f"Game Over! LOSER You made {errors_count} errors.", True, (255, 0, 0))
        surface.blit(game_over_text, (150, 75))  
        
        
        pygame.display.update()
        time.sleep(2)  
        reset_game(level)
        return "game_over"  
    
    return None  

def draw_time(surface, start_time):
    if start_time is None:
        start_time = time.time()

    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, black)
    surface.blit(time_text, (450, 10))

def draw_grid():
    for row in range(9):
        for col in range(9):
            pygame.draw.rect(Window, (255, 255, 255), (start_x + col * cell_size, start_y + row * cell_size, cell_size, cell_size))
    for i in range(0, 10):
        thickness = 4 if i % 3 == 0 else 2
        pygame.draw.line(Window, black, (start_x + i * cell_size, start_y), (start_x + i * cell_size, start_y + grid_height), thickness)
        pygame.draw.line(Window, black, (start_x, start_y + i * cell_size), (start_x + grid_width, start_y + i * cell_size), thickness)

def draw_numbers(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] != 0:
                num_text = font.render(str(board[row][col]), True, black)
                Window.blit(num_text, (start_x + col * cell_size + (cell_size - num_text.get_width()) // 2,
                                       start_y + row * cell_size + (cell_size - num_text.get_height()) // 2))

def validBoard(board, number, cell):
    row, col = cell
    for i in range(9):
        if board[row][i] == number or board[i][col] == number:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == number:
                return False
    return True

def check_win(board):
    for row in board:
        for cell in row:
            if cell == 0:
                return False
    return True

def set_difficulty(level):
    global board
    if level == "easy":
        board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        locked_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]

    elif level == "medium":
        board = [
            [0, 0, 0, 2, 0, 0, 7, 0, 1],
            [6, 8, 0, 0, 7, 0, 0, 9, 0],
            [1, 9, 0, 0, 0, 4, 5, 0, 0],
            [8, 2, 0, 1, 0, 0, 0, 4, 0],
            [0, 0, 0, 6, 0, 2, 9, 0, 0],
            [0, 5, 0, 0, 0, 3, 0, 2, 8],
            [0, 0, 9, 3, 0, 0, 0, 7, 4],
            [0, 4, 0, 0, 5, 0, 0, 3, 6],
            [0, 0, 3, 0, 1, 8, 0, 0, 0]
        ]
        locked_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]

    elif level == "hard":
        board = [
            [0, 0, 0, 6, 0, 0, 4, 0, 0],
            [7, 0, 0, 0, 0, 3, 6, 0, 0],
            [0, 0, 0, 0, 9, 1, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 1, 8, 0, 0, 0, 3],
            [0, 0, 0, 3, 0, 6, 0, 4, 5],
            [0, 4, 0, 2, 0, 0, 0, 6, 0],
            [9, 0, 3, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 0, 1, 0, 0]
        ]
        locked_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]

current_screen = "main_menu"
board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
locked_cells = [(row, col) for row in range(9) for col in range(9) if board[row][col] != 0]

loop = True
while loop:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

        if current_screen == "main_menu":
            if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse_pos):
                current_screen = "level_selection"

        elif current_screen == "level_selection":
            if event.type == pygame.MOUSEBUTTONDOWN:
                for level, rect in level_buttons.items():
                    if rect.collidepoint(mouse_pos):
                        set_difficulty(level)
                        current_screen = "game_screen"
                        errors_count = 0
                        start_time = time.time()

        elif current_screen == "game_screen":
            if event.type == pygame.MOUSEBUTTONDOWN:
                select_number.handle_click(event.pos)
            if event.type == pygame.MOUSEMOTION:
                select_number.handle_drag(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                select_number.handle_release(event.pos, board, locked_cells)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                current_screen = "main_menu"

    if current_screen == "main_menu":
        Window.blit(background, (0, 0))
        Window.blit(text_1, text_1_rect)
        Window.blit(text_2, text_2_rect)

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(Window, hover_color, button_rect, border_radius=15)
        else:
            pygame.draw.rect(Window, button_color, button_rect, border_radius=15)

        Window.blit(button_text, button_text.get_rect(center=button_rect.center))

    elif current_screen == "level_selection":
        Window.fill(ofwhite)
        for level, rect in level_buttons.items():
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(Window, hover_color, rect, border_radius=15)
            else:
                pygame.draw.rect(Window, button_color, rect, border_radius=15)
            Window.blit(level_texts[level], level_texts[level].get_rect(center=rect.center))

    elif current_screen == "game_screen":
        Window.fill(ofwhite)
        draw_grid()
        draw_numbers(board)
        select_number.draw(Window)
        game_over = draw_errors(Window, errors_count, max_errors)  

        draw_time(Window, start_time)

        if check_win(board):
            win_text = font.render("This's the right solution.", True, (0, 225, 0))
            Window.blit(win_text, (225, 75))
            pygame.display.update()
            time.sleep(2)
           

        if game_over == "game_over":
            select_number.dragging = False
            select_number.selected_number = 0
            select_number.dragged_number = 0
            reset_game(level)

    pygame.display.update()

pygame.quit()
sys.exit()