#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
An AI player for Othello.

@author: Eve Rigley
"""

import random
import sys
import time
from datetime import timedelta, datetime

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

######MY HERUSTICS FUNCTIONS##############################################################
#

def isCorner(board, x, y):
    corner_locations = [(0, 0), (len(board) - 1, len(board) - 1), (0, len(board) - 1), (len(board) - 1, 0)]
    if (x, y) in corner_locations:
        return True

def isInvincible(board, color, x, y, direction):
    if isCorner(board, x, y):
        return True

    elif x == len(board) - 1 or x == 0:
        if direction == 0 or direction == -1:
            if board[y - 1][x] == color:
                is_invincible = isInvincible(board, color, x, y - 1, -1)
                if is_invincible == True:
                    return is_invincible

        if direction == 0 or direction == 1:
            if board[y + 1][x] == color:
                return isInvincible(board, color, x, y + 1, 1)

    elif y == len(board) - 1 or y == 0:

        if direction == 0 or direction == -1:
            if board[y][x - 1] == color:
                is_invincible = isInvincible(board, color, x - 1, y, -1)
                if is_invincible == True:
                    return is_invincible

        if direction == 0 or direction == 1:
            if board[y][x + 1] == color:
                return isInvincible(board, color, x + 1, y, 0)

    return False

def coin_diff(board):
    """Measures the difference in the number of pieces on board."""
    p1_count, p2_count = get_score(board)
    coin_total = p1_count + p2_count
    p1_coin_diff = 100 * (p1_count/coin_total)
    p2_coin_diff = 100 * (p2_count/coin_total)
    return p1_coin_diff, p2_coin_diff


def choice_diff(board):
    """Measures the difference in the choice_diff in terms of available choices."""
    p1_moves_num = len(get_possible_moves(board,1))
    p2_moves_num = len(get_possible_moves(board,2))
    moves_total = p1_moves_num + p2_moves_num
    if (p1_moves_num + p2_moves_num) != 0:
        p1_choice_diff = 100 * (p1_moves_num/moves_total)
        p2_choice_diff = 100 * (p2_moves_num/moves_total)
    else:
        p1_choice_diff = 0
        p2_choice_diff = 0
    return p1_choice_diff, p2_choice_diff


def corner_diff(board):
    """Measures the difference in the number of corners captured."""
    p1_corner = 0
    p2_corner = 0
    #corners = [(0,0),(0,7),(7,0),(7,7)]
    x = [0,0,7,7]
    y = [0,7,0,7]
    for i,j in zip(x,y):
        if board[i][j] == 1:
            p1_corner += 1
        elif board[i][j] == 2:
            p2_corner += 1
    total_corner = p1_corner + p2_corner
    if (p1_corner + p2_corner) != 0:
        p1_corner_diff = 100 * (p1_corner/total_corner)
        p2_corner_diff = 100 * (p2_corner/total_corner)
    else:
        p1_corner_diff = 0
        p2_corner_diff = 0
    return p1_corner_diff, p2_corner_diff
#
def stability_diff(board):
    """Measures the board heuristic"""
    #To be added later to reduce intial complexity
    p1_stability = 0
    p2_stability = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                if isInvincible(board, 1, j, i, 0):
                    p1_stability += 1
            elif board[i][j] == 2:
                if isInvincible(board, 2, j, i, 0):
                    p2_stability += 1
    stability_total = p1_stability + p2_stability
    if (p1_stability + p2_stability) != 0:
        p1_stability_diff = 100 * (p1_stability/stability_total)
        p2_stability_diff = 100 * (p2_stability/stability_total)
    else:
        p1_stability_diff = 0
        p2_stability_diff = 0
    return p1_stability_diff, p2_stability_diff

#################UTILITY & HEURISTICS###################################################################

corners = [(0,0),(0,7),(7,0),(7,7)]

def compute_utility(board, color):
    return 0

def get_score_weighted(board):

    p1_coin_diff, p2_coin_diff = coin_diff(board)
    p1_choice_diff, p2_choice_diff = choice_diff(board)
    p1_corner_diff, p2_corner_diff = corner_diff(board)
    p1_stability_diff, p2_stability_diff = stability_diff(board)

    p1_adj_weight = (0.15 * p1_coin_diff + 0.15 * p1_choice_diff + 0.4 * p1_corner_diff + 0.3 * p1_stability_diff)
    p2_adj_weight = (0.15 * p2_coin_diff + 0.15 * p2_choice_diff + 0.4 * p2_corner_diff + 0.3 * p2_stability_diff)

    return p1_adj_weight, p2_adj_weight

############ MINIMAX ###############################

def minimax_min_node(board, color, depth, end_time):
    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then ai player is white
            return score[1]-score[0] #score for ai black
        else:
            return score[0]-score[1] #score for ai white
    else:
        if color == 1:
            next_color = 2
        else:
            next_color = 1
        best_min_score = 1000000
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            move_score = minimax_max_node(new_board, next_color, depth-1, end_time)
            if move_score < best_min_score:
                best_min_score = move_score
        return best_min_score
    return None


def minimax_max_node(board, color, depth, end_time):
    possible_moves = get_possible_moves(board, color)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then ai player is black
            return score[0]-score[1] #score for ai black
        else:
            return score[1]-score[0] #score for ai white
    else:
        if color == 1:
            next_color = 2
        else:
            next_color = 1

        best_max_score = -1000000
        for move in possible_moves:
            new_board = play_move(board, color, move[0], move[1])
            move_score = minimax_min_node(new_board, next_color, depth-1, end_time)
            if move_score > best_max_score:
                best_max_score = move_score
        return best_max_score
    return None


def select_move_minimax(board, color, depth, end_time):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    best_max_score = -10000000

    possible_moves = get_possible_moves(board, color)

    if color == 1:
        next_color = 2
    else:
        next_color = 1

    for move in possible_moves:
        #return move[0], move[1] #SPECIAL RETURM SEE IF ITS WORKING
        new_board = play_move(board, color, move[0], move[1])
        move_score = minimax_min_node(new_board, next_color, depth-1, end_time)
        if move_score > best_max_score:
            best_max_score = move_score
            best_move = move
    return best_move

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, depth, alpha, beta, end_time, debug_mode):

    possible_moves = get_possible_moves(board, color)
    if debug_mode:
        print("Starting Min")
        print(possible_moves)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then min is black, so ai player is white
            return score[1]-score[0] #score for ai white
        else:
            return score[0]-score[1] #score for ai black
    else:
        if color == 1:
            next_color = 2
        else:
            next_color = 1
        best_min_score = 1000000
        for move in possible_moves:
            if move in corners:
                if debug_mode:
                    print("In min - playing a corner")
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: #then min is black, so ai player is white
                    return score[1]-score[0] #score for ai white
                else:
                    return score[0]-score[1] #score for ai black

            if debug_mode:
                print("MIN Playing Move: (" + str(move[0]) + ", " + str(move[1])+")")

            new_board = play_move(board, color, move[0], move[1])

            move_score = alphabeta_max_node(new_board, next_color, depth-1, alpha, beta, end_time, debug_mode)
            if debug_mode:
                print("In Min: Move Score " + str(move_score)+ " for (" + str(move[0]) + ", " + str(move[1]) + ")")

            if move_score < best_min_score:
                best_min_score = move_score
                beta = min(beta, move_score)
            if beta <= alpha:
                break
        #print("In Min: Returning Lowest Move Score" + str(best_min_score))
        return best_min_score
    return None


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, depth, alpha, beta, end_time, debug_mode):

    if debug_mode:
        print("Starting Max")

    possible_moves = get_possible_moves(board, color)
    if debug_mode:
        print("Starting Max")
        print(possible_moves)
    current_time = datetime.now()
    if possible_moves == [] or depth==0 or current_time >= end_time:
        score = get_score_weighted(board) #get_score(board)
        if color == 1: #then ai player is black
            return score[0]-score[1] #score for ai black
        else:
            return score[1]-score[0] #score for ai white
    else:
        if color == 1:
            next_color = 2
        else:
            next_color = 1

        best_max_score = -1000000
        for move in possible_moves:
            if move in corners:
                if debug_mode:
                    print("In max - playing a corner")
                new_board = play_move(board, color, move[0], move[1])
                score = get_score_weighted(new_board)
                if color == 1: #then ai player is black
                    return score[0]-score[1] #score for ai black
                else:
                    return score[1]-score[0] #score for ai white
            if debug_mode:
                print("MAX Playing Move: (" + str(move[0]) + ", " + str(move[1])+")")

            new_board = play_move(board, color, move[0], move[1])
            move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time, debug_mode)
            if debug_mode:
                print("In Max: Move Score " + str(move_score)+ " for (" + str(move[0]) + ", " + str(move[1]) +")")
            if move_score > best_max_score:
                best_max_score = move_score
                alpha = max(alpha, move_score)
            if beta <= alpha:
                break

        if debug_mode:
            print("In Max: Returning Best Move Score " + str(best_max_score))

        return best_max_score
    return None


def select_move_alphabeta(board, color, depth, end_time, debug_mode):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    best_max_score = -10000000
    alpha = -1000000
    beta = 1000000


    possible_moves = get_possible_moves(board, color)
    if debug_mode:
        print("-----------------------Starting Select---------------------------")
        print(possible_moves)

    if color == 1:
        next_color = 2
    else:
        next_color = 1

    for move in possible_moves:
        #return move[0], move[1] #SPECIAL RETURN SEE IF ITS WORKING
        if move in corners:
            return move
        if debug_mode:
            print("SELECT Playing Move: (" + str(move[0]) + ", " + str(move[1])+")")
        new_board = play_move(board, color, move[0], move[1])
        move_score = alphabeta_min_node(new_board, next_color, depth-1, alpha, beta, end_time, debug_mode)
        if debug_mode:
            print("In Select: Move Score" + str(move_score))

        if move_score > best_max_score:
            best_max_score = move_score
            best_move = move

    if debug_mode:
        print("In Select: Returning Best Move Score" + str(best_max_score))

    return best_move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    debug_mode = False

    print("Killer AI (c)") # First line is the name of this AI
    if debug_mode:
        color = 1
    else:
        color = int(input()) # Then we read the color: 1 for dark (goes first),
        # 2 for light.


    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        if debug_mode:
            next_input = 1 #input()
            #status, dark_score_s, light_score_s = next_input.strip().split()
            status = "SCORE"
            dark_score = 2#int(dark_score_s)
            light_score = 2#int(light_score_s)
            current_time = datetime.now()
            end_time = current_time + timedelta(seconds=15)
        else:
            next_input = input()
            status, dark_score_s, light_score_s = next_input.strip().split()
            dark_score = int(dark_score_s)
            light_score = int(light_score_s)
            current_time = datetime.now()
            end_time = current_time + timedelta(seconds=4.5)

        if status == "FINAL": # Game is over.
            print
        else:
            if debug_mode:
                board =[
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 2, 2, 2, 0, 0, 0],
                    [0, 0, 0, 2, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0]]
            else:
                board = eval(input()) # Read in the input and turn it into a Python
                # object. The format is a list of rows. The
                # squares in each row are represented by
                # 0 : empty square
                # 1 : dark disk (player 1)
                # 2 : light disk (player 2)

            # Select the move and send it to the manager
            #movei, movej = select_move_minimax(board, color, 5) #Choose depth
            movei, movej = select_move_alphabeta(board, color, 5, end_time, debug_mode) #Choose depth

            print("{} {}".format(movei, movej))

        if debug_mode:
            break

if __name__ == "__main__":
    run_ai()


