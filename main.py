import pygame

pygame.init()

WINDOW_SIZE = (630, 630)
CELL_SIZE = WINDOW_SIZE[0] // 9

GRID_COLOR = (255, 255, 255)
CELL_COLOR = (100, 100, 100)
SMALL_XOCOLOR = (0, 0, 0)
BIG_XOCOLOR = (255, 0, 0)
OUT_COLOR = (0, 0, 255)

main_board = [[' ' for _ in range(3)] for _ in range(3)]
small_boards = [[[[' ' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
font = pygame.font.Font(None, 100)
big_font = pygame.font.Font(None, 300)

window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Super Tic Tac Toe')

player_turn = 'X'  # Player X always goes first

def draw_board(screen, main_board, small_boards):
    screen.fill(GRID_COLOR)  # Fill the screen with the grid color

    # Draw the main board grid
    for i in range(1, 4):
        pygame.draw.line(screen, CELL_COLOR, (i * CELL_SIZE*3, 0), (i * CELL_SIZE*3, WINDOW_SIZE[1]), 5)
        pygame.draw.line(screen, CELL_COLOR, (0, i * CELL_SIZE*3), (WINDOW_SIZE[0], i * CELL_SIZE*3), 5)

    # Draw the smaller Tic Tac Toe boards within the main board
    for row in range(3):
        for col in range(3):
            # Calculate the position for each smaller board
            x = col * CELL_SIZE * 3
            y = row * CELL_SIZE * 3

            # Draw the grid for each smaller board
            for i in range(1, 4):
                pygame.draw.line(screen, CELL_COLOR, (x + i * CELL_SIZE, y), (x + i * CELL_SIZE, y + CELL_SIZE * 3), 2)
                pygame.draw.line(screen, CELL_COLOR, (x, y + i * CELL_SIZE), (x + CELL_SIZE * 3, y + i * CELL_SIZE), 2)

            # Display the content of each smaller board (Xs and Os)
            for i in range(3):
                for j in range(3):
                    cell_content = small_boards[row][col][i][j]
                    if cell_content != ' ':
                        text = font.render(cell_content, True, SMALL_XOCOLOR)
                        text_rect = text.get_rect(center=(x + j * CELL_SIZE + CELL_SIZE // 2,
                                                        y + i * CELL_SIZE + CELL_SIZE // 2))
                        screen.blit(text, text_rect)
            
            cell_content = main_board[row][col]
            if cell_content != ' ':
                text = big_font.render(cell_content, True, BIG_XOCOLOR)
                text_rect = text.get_rect(center=(col * CELL_SIZE*3 + CELL_SIZE*3 // 2,
                                                row * CELL_SIZE*3 + CELL_SIZE*3 // 2))
                screen.blit(text, text_rect)
    
    pygame.display.flip()

def handle_click(pos):
    global player_turn
    
    x, y = pos
    clicked_row = y // CELL_SIZE
    clicked_col = x // CELL_SIZE

    if small_boards[clicked_row//3][clicked_col//3][clicked_row%3][clicked_col%3] != ' ':
        return
    small_boards[clicked_row // 3][clicked_col // 3][clicked_row % 3][clicked_col % 3] = player_turn
    player_turn = 'X' if player_turn == 'O' else 'O'
    

    if main_board[clicked_row//3][clicked_col//3] == ' ':
        main_board[clicked_row//3][clicked_col//3] = check_win(small_boards[clicked_row//3][clicked_col//3])
    
    a = check_win(main_board)
    
    if a != ' ':
        return True
    
    

def check_win(board):
    # Check if any of the players have won the game
    # Return the winning player or ' ' if there is no winner
    
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
        
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    # Check for a draw
    if ' ' not in board[0] and ' ' not in board[1] and ' ' not in board[2]:
        return 'D'
                
    return ' '

def display_outcome(screen, outcome):
    # Display a message when a player wins or when the game ends in a draw
    # Use pygame.font.Font() and render text to display the outcome message
    
    if outcome == 'D':
        text = big_font.render('Draw!', True, OUT_COLOR)
    else:
        text = big_font.render(str(outcome) + ' wins!', True, OUT_COLOR)
    text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    screen.blit(text, text_rect)

running = True
playing = True
while running:
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if handle_click(mouse_pos):
                    playing = False
    
        draw_board(window, main_board, small_boards)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    
    if check_win(main_board) != ' ': display_outcome(window, check_win(main_board))
    pygame.display.flip()
    

# Quit Pygame
pygame.quit()