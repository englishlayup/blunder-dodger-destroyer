# library: https://github.com/PySimpleGUI (demo provided)
import PySimpleGUI as sg
import os
import chess


# piece imgs stored in pieces folder
PATH = 'pieces/'

# get img paths
# imgs from https://commons.wikimedia.org/wiki/Chess_pieces
blank = os.path.join(PATH, 'blank.png')
black_pawn = os.path.join(PATH, 'black_pawn.png')
black_knight = os.path.join(PATH, 'black_knight.png')
black_bishop = os.path.join(PATH, 'black_bishop.png')
black_rook = os.path.join(PATH, 'black_rook.png')
black_king = os.path.join(PATH, 'black_king.png')
black_queen = os.path.join(PATH, 'black_queen.png')
white_pawn = os.path.join(PATH, 'white_pawn.png')
white_knight = os.path.join(PATH, 'white_knight.png')
white_bishop = os.path.join(PATH, 'white_bishop.png')
white_rook = os.path.join(PATH, 'white_rook.png')
white_king = os.path.join(PATH, 'white_king.png')
white_queen = os.path.join(PATH, 'white_queen.png')

# constants
BLANK = 0
BLACK_PAWN = 1
BLACK_KNIGHT = 2
BLACK_BISHOP = 3
BLACK_ROOK = 4
BLACK_KING = 5
BLACK_QUEEN = 6
WHITE_PAWN = 7
WHITE_KNIGHT = 8
WHITE_BISHOP = 9
WHITE_ROOK = 10
WHITE_KING = 11
WHITE_QUEEN = 12

imgs = {BLANK: blank,
        BLACK_PAWN: black_pawn,
        BLACK_KNIGHT: black_knight,
        BLACK_BISHOP: black_bishop,
        BLACK_ROOK: black_rook,
        BLACK_KING: black_king,
        BLACK_QUEEN: black_queen,
        WHITE_PAWN: white_pawn,
        WHITE_KNIGHT: white_knight,
        WHITE_BISHOP: white_bishop,
        WHITE_ROOK: white_rook,
        WHITE_KING: white_king,
        WHITE_QUEEN: white_queen}


# square colors
def square(image, key, spot):
    if (spot[0] + spot[1]) % 2:
        color = '#cc6600'  # dark
    else:
        color = '#ffffcc'  # light

    return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=key)


def redraw(win, visual_board):
    for rank in range(8):
        for file in range(8):
            if (rank + file) % 2:
                color = '#cc6600'
            else:
                color = '#ffffcc'

            piece_img = imgs[visual_board[rank][file]]

            element = win.FindElement(key=(rank, file))
            element.Update(button_color=('white', color), image_filename=piece_img)


def play():
    # background is system default
    sg.ChangeLookAndFeel('SystemDefault')

    # GUI board represented by constants
    # not actual board
    visual_board = [
        [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_KING, BLACK_QUEEN, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
        [BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN, BLACK_PAWN],
        [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
        [BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK, BLANK],
        [WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN],
        [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_KING, WHITE_QUEEN, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
        ]

    # top letter coordinates
    layout = [[sg.T('{}'.format(letter), pad=((30, 28), 0)) for letter in 'abcdefgh']]

    for row in range(8):
        # number coordinates at start of rank
        rank = [sg.T(str(8 - row) + ' ')]

        # add square to rank
        for col in range(8):
            piece_img = imgs[visual_board[row][col]]
            rank.append(square(piece_img, key=(row, col), spot=(row, col)))

        # number coordinates at end of rank
        rank.append(sg.T(str(8 - row) + ' '))

        layout.append(rank)

    # bottom letter coordinates
    layout.append([sg.T('{}'.format(letter), pad=((30, 28), 0)) for letter in 'abcdefgh'])

    # create window
    win = sg.Window('COSC4426AE-21F - Project').Layout(layout)

    # actual chess board represented by chess's board class
    board = chess.Board()

    # initialize game variables
    moving = False
    move_from = move_to = 0

    # game loop
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            moving = False

            while True:
                event, value = win.Read()

                if isinstance(event, tuple):
                    if moving == False:
                        # get coordinates of piece player clicked on
                        move_from = event
                        rank = move_from[0];
                        file = move_from[1]

                        # get piece from board
                        piece = visual_board[rank][file]

                        # red visual cue
                        button_square = win.FindElement(key=(rank, file))
                        button_square.Update(button_color=('white', 'red'))

                        # piece can now move
                        moving = True

                    # piece can be moved
                    elif moving == True:
                        # coordinates of move location
                        move_to = event
                        rank = move_to[0];
                        file = move_to[1]

                        # player clicked on same square
                        if move_to == move_from:
                            if (rank + file) % 2:
                                color = '#cc6600'
                            else:
                                color = '#ffffcc'

                            button_square.Update(button_color=('white', color))

                            moving = False

                            continue

                        # convert to python-chess notation
                        # e.g., e2e4 means move from e2 to e4
                        move = '{}{}{}{}'.format('abcdefgh'[move_from[1]], 8 - move_from[0],
                                                 'abcdefgh'[move_to[1]], 8 - move_to[0])

                        # legal move
                        if move in [str(move) for move in board.legal_moves]:
                            board.push(chess.Move.from_uci(move))
                        # illegal move
                        else:
                            moving = False

                            if (move_from[0] + move_from[1]) % 2:
                                color = '#cc6600'
                            else:
                                color = '#ffffcc'

                            button_square.Update(button_color=('white', color))

                            continue

                        # move piece and redraw board
                        visual_board[move_from[0]][move_from[1]] = BLANK
                        visual_board[rank][file] = piece
                        redraw(win, visual_board)

                        break

        # engine's turn
        else:
            # IMPLEMENT ENGINE GAMEPLAY HERE
            board.turn = chess.WHITE


if __name__ == '__main__':
    play()
