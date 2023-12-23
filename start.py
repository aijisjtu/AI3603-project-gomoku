# -*- coding: utf-8 -*-

'''
本文件是多余文件！extra file。不正式提交，只在提交前用于辅助测试
实际上不需要实现人与mcts_player对战，也不需要人与深度学习训练后的player对战
但是可以方便测试棋盘显示功能
'''


from __future__ import print_function
from collections import OrderedDict
import pickle
import torch

from game import Board, Game
from mcts_enhanced import MCTSPlayer
# from mcts_pure import MCTSPlayer as MCTS_Pure
from policy_value_net import PolicyValueNet  # Pytorch


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run():
    n = 5
    width, height = 8, 8
    model_file = 'best_policy.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        # ############### human VS AI ###################
        # uncomment the following two lines load the trained policy_value_net in PyTorch

        best_policy = PolicyValueNet(width, height, model_file=model_file)

        mcts_player = MCTSPlayer(
            best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)

        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')


if __name__ == '__main__':
    run()
