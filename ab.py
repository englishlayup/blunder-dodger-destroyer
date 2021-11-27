#importing libraries
import random
from IPython.display import clear_output, display
import time
import chess
import numpy as np
import itertools

piece_value_map = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 10000
}

def cal_material(observation, turn):
    total = 0

    #number of pawns
    total += len(observation.pieces(chess.PAWN, turn)) * piece_value_map[chess.PAWN]
    #number of white knights
    total += len(observation.pieces(chess.KNIGHT, turn)) * piece_value_map[chess.KNIGHT]
    #number of bishops
    total += len(observation.pieces(chess.BISHOP, turn)) * piece_value_map[chess.BISHOP]
    #number of rooks
    total += len(observation.pieces(chess.ROOK, turn)) * piece_value_map[chess.ROOK]
    #number of queens
    total += len(observation.pieces(chess.QUEEN, turn)) * piece_value_map[chess.QUEEN]

    return total


#function to evaluate the board
def evaluate_board(observation):
    #get sum of both sides points
    white_eval = cal_material(observation, chess.WHITE)
    black_eval = cal_material(observation, chess.BLACK)

    #Negative board value means black is leading, positive means white
    evaluation = white_eval - black_eval

    #if it is black's turn flip the sign to reflect black's evaluation
    perspective = 1
    if not observation.turn:
        perspective *= -1

    return evaluation*perspective

    #end result will be:
        #if it is white's turn, positive is better negative is better
        #if it is black's turn, positive is better and negative is better

#Search Function
def search(observation, depth, alpha, beta):

    if depth == 0:
        return search_all_captures(observation, alpha, beta)
    if observation.is_checkmate():
        return -1e9
    if observation.is_stalemate():
        return 0

    moves = list(observation.legal_moves)
    moves.sort(key=lambda x: eval_move(observation, x), reverse=True)

    for move in moves:
        observation.push(move)
        evaluation = -search(observation, depth-1, -beta, -alpha)
        observation.pop()
        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

    return alpha

def eval_move(board, move):
    move_score = 0
    move_piece = board.piece_type_at(move.from_square)
    capture_piece = board.piece_type_at(move.to_square)

    if capture_piece:
        move_score = 10 * piece_value_map[capture_piece] - piece_value_map[move_piece]

    if move.promotion:
        move_score += piece_value_map[move.promotion]

    enemy_pawn_squares = board.pieces(chess.PAWN, not board.turn)
    attacked_by_pawns = list(itertools.chain.from_iterable(map(board.attacks, enemy_pawn_squares)))
    if move.to_square in attacked_by_pawns:
        move_score -= piece_value_map[move_piece]

    return move_score

def search_all_captures(observation, alpha, beta):
        evaluation = evaluate_board(observation)

        if evaluation >= beta:
            return beta
        alpha = max(alpha, evaluation)

        capture_moves = [x for x in observation.legal_moves if observation.is_capture(x)]

        for move in capture_moves:

            observation.push(move)
            evaluation = -search_all_captures(observation, -beta, -alpha)
            observation.pop()

            if evaluation >= beta:
                return beta
            alpha = max(alpha, evaluation)

        return alpha

class AlphaBetaAgent:
    def alpha_beta_search(self, board, depth):
        evaluations = list()
        for move in board.legal_moves:
            board.push(move)
            evaluations.append((move, -search(board, depth-1, -1e9, 1e9)))
            board.pop()
        return max(evaluations, key=lambda x: x[1])[0]
