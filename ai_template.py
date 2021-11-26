#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
An AI player for Othello. This is the template file that you need to  
complete and submit for the competition. 

@author: YOUR NAME
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI 
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def compute_utility(board, color):
    return 0


############ MINIMAX ###############################

move_dictionary = dict()

############ MINIMAX ###############################

def minimax_max_node(board, color, depth):
    possible_moves = get_possible_moves(board, color)
    move_states = {move: play_move(board, color, move[0], move[1]) for move in possible_moves}
    best_move = None
    best_value = None

    if len(possible_moves) > 0:
        if depth == 1:
            for move, state in move_states.items():
                if best_move == None or minimax_min_node(state, color, depth + 1) > best_value:
                    best_move = move
                    best_value = minimax_min_node(state, color, depth + 1)

            return best_move

        else:
            for move, state in move_states.items():

                if best_move == None or minimax_min_node(state, color, depth + 1) > best_value:
                    best_value = minimax_min_node(state, color, depth + 1)

            return best_value
    return compute_utility(board, color)


def minimax_min_node(board, color, depth):
    other_color = 1 if color == 2 else 2
    possible_moves = get_possible_moves(board, other_color)
    move_states = {move: play_move(board, other_color, move[0], move[1]) for move in possible_moves}
    best_move = None
    best_value = None

    if len(possible_moves) > 0:
        if depth <= 3:
            for move, state in move_states.items():

                if best_move == None or minimax_max_node(state, color, depth + 1) < best_value:
                    best_move = move
                    best_value = minimax_max_node(state, color, depth + 1)

            return best_value

        else:
            for move, state in move_states.items():

                if best_value == None or compute_utility(state, color) < best_value:
                    best_value = compute_utility(state, color)

            return best_value
    return compute_utility(board, color)

    
def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  
    """
    return 0,0 
    

def run_ai():
    """
    This function establishes communication with the game manager. 
    It first introduces itself and receives its color. 
    Then it repeatedly receives the current score and current board state
    until the game is over. 
    """
    print("Minimax AI") # First line is the name of this AI  
    color = int(input()) # Then we read the color: 1 for dark (goes first), 
                         # 2 for light. 

    while True: # This is the main loop 
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input() 
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over. 
            print 
        else: 
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The 
                                  # squares in each row are represented by 
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)
                    
            # Select the move and send it to the manager 
            movei, movej = select_move_minimax(board, color)
           
            print("{} {}".format(movei, movej)) 


if __name__ == "__main__":
    run_ai()