import pygame
import sys
import time

import tictactoe as ttt

pygame.init()
size = width, height = 600, 400

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
aggieBlue = (0, 45, 116)
aggieGold = (253, 184, 39)

screen = pygame.display.set_mode(size,pygame.RESIZABLE)

mediumFont = pygame.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pygame.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pygame.font.Font("OpenSans-Regular.ttf", 60)

user = None
userColor = None
board = ttt.initial_state()
ai_turn = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)
            screen = pygame.display.set_mode((size), pygame.RESIZABLE)

    screen.fill(black)

    # Let user choose a player.
    if user is None:

        # Draw title
        title = largeFont.render("Play Tic-Tac-Toe", True, white)
        titleRect = title.get_rect()
        titleRect.center = (size[0] / 2, 50)
        #titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Draw buttons
        #playXButton = pygame.Rect((width / 8), (height / 2), width / 4, 50)
        playXButton = pygame.Rect(size[0] / 8, (size[1] / 2), size[0] / 4, 50)
        playX = mediumFont.render("Play as X", True, black)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(screen, white, playXButton, 0, 30, 30, 30, 30)
        screen.blit(playX, playXRect)

        playOButton = pygame.Rect(5 * size[0] / 8, (size[1] / 2), size[0] / 4, 50)
        #playOButton = pygame.Rect(5 * (width / 8), (height / 2), width / 4, 50)
        playO = mediumFont.render("Play as O", True, black)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(screen, white, playOButton, 0, 30, 30, 30, 30)
        screen.blit(playO, playORect)

        # Check if button is clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.X
                userColor = aggieGold
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                user = ttt.O
                userColor = aggieBlue

    else:

        # Draw game board
        tile_size = size[0] / 9
        #tile_size = 80
        tile_origin = (size[0] / 2 - (1.5 * tile_size),
                       size[1] / 2 - (1.5 * tile_size))
            #tile_origin = (width / 2 - (1.5 * tile_size),
            #         height / 2 - (1.5 * tile_size))
        tiles = []
        for i in range(3):
            row = []
            for j in range(3):
                rect = pygame.Rect(
                    tile_origin[0] + j * tile_size,
                    tile_origin[1] + i * tile_size,
                    tile_size, tile_size
                )
                pygame.draw.rect(screen, white, rect, 3)

                if board[i][j] != ttt.EMPTY:
                    #switch color for X and O
                    if board[i][j] == ttt.X:
                        userColor = aggieGold
                    else:
                        userColor = aggieBlue
                    move = moveFont.render(board[i][j], True, userColor)
                    moveRect = move.get_rect()
                    moveRect.center = rect.center
                    screen.blit(move, moveRect)
                row.append(rect)
            tiles.append(row)
    
        game_over = ttt.terminal(board)
        player = ttt.player(board)

        # Show title
        if game_over:
            winner = ttt.winner(board)
            if winner is None:
                title = f"Game Over: Tie."
            else:
                title = f"Game Over: {winner} wins."
        elif user == player:
            title = f"Play as {user}"
        else:
            title = f"Computer thinking..."
        title = largeFont.render(title, True, white)
        titleRect = title.get_rect()
        titleRect.center = ((size[0] / 2), 30)
        #titleRect.center = ((width / 2), 30)
        screen.blit(title, titleRect)

        # Check for AI move
        if user != player and not game_over:
            if ai_turn:
                time.sleep(0.5)
                move = ttt.minimax(board)
                board = ttt.result(board, move)
                ai_turn = False
            else:
                ai_turn = True

        # Check for a user move
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                for j in range(3):
                    if (board[i][j] == ttt.EMPTY and tiles[i][j].collidepoint(mouse)):
                        board = ttt.result(board, (i, j))

        if game_over:
            againButton = pygame.Rect(size[0] / 3, size[1] - 65, size[0] / 3, 50)
            #againButton = pygame.Rect(width / 3, height - 65, width / 3, 50)
            again = mediumFont.render("Play Again", True, black)
            againRect = again.get_rect()
            againRect.center = againButton.center
            pygame.draw.rect(screen, white, againButton)
            screen.blit(again, againRect)
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if againButton.collidepoint(mouse):
                    time.sleep(0.2)
                    user = None
                    board = ttt.initial_state()
                    ai_turn = False
                        
    pygame.display.flip()
