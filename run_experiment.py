import pygame.display
import time
import random
import os
import itertools
from main import run_visualization
from displays import *
from config import observation_space_size_x, observation_space_size_y, scaling, edge
from actr import rpc_interface
from actr.socket_manager import comet_socket, move_socket
import threading

import asyncio
# participant code
code = input('Enter code: ')

# initialize pygame
# how many frames per second
FPS = 60

# pygame general setup
pygame.init()

# initialize pygame display
screen_width = (observation_space_size_x + (2 * edge)) * scaling
screen_height = observation_space_size_y * scaling
screen = pygame.display.set_mode((screen_width, screen_height))  # ,pygame.FULLSCREEN vs. pygame.RESIZABLE

# initialize practice procedure
# practice_trials = ['training1', 'training2', 'training3', 'training4', 'training5']
practice_trials = ['training1']
practice_drift_enabled_args = [False]  # [False, False, False]
practice_input_noise_args = [0]  # [0, 0, 0]
practice_args_list = [practice_trials, practice_drift_enabled_args, practice_input_noise_args]
practice_arg_combs = list(itertools.product(*practice_args_list))
# COMING: HAVE all args combined only with the exact iterable to have more control over subsequent practice trials
practice_attempt_dict = dict.fromkeys(practice_arg_combs, 0)  # every trial at 0 attempts
practice_list_of_attempt_dict_keys = list(practice_attempt_dict.keys())

# initialize experimental procedure
# N_trials = 3  # for each trial there must be a drift_ranges, object_list, and walls_dict file in the logs folder
# trials = list(range(1, N_trials + 1))  # end +1 due to python stopping before processing last entry
# trials = [1, 2, 3]  # simply stating every level in a list is also possible
trials = [0]

# drift enabled
# drift_enabled_args = [True, False]
drift_enabled_args = [True]

# input noise
# input_noise_args = [0, 0.5, 1, 1.5, 2]
input_noise_args = [0]


# create list of all possible combinations of level and control manipulations
args_list = [trials, drift_enabled_args, input_noise_args]
arg_combs = list(itertools.product(*args_list))
# order of args:
# [0]: trial; [1]: drift; [2]: input noise

# attempts_dict for monitoring attempts per trial
attempt_dict = dict.fromkeys(arg_combs, 0)  # every trial at 0 attempts
list_of_attempt_dict_keys = list(attempt_dict.keys())
# list_of_attempt_dict_keys is our loop object. We will remove trials from here when they are attempted 3 times already
# or have been solved completely

max_attempts = 1  # maximum number of attempts given to solve trial


# start experimental procedure
quit = False
level_done = False
instructions = False
n_run = 0


    # Send move-left
message2 = '{"method": "add", "params":["moveleft", "moveleft", "this documents moveleft"], "id": 1}'

print(f"message2: {message2}")
#socket.setblocking(False)
received = rpc_interface.communicate_socket(move_socket, message2)
print(f"received: {received}")

# Send move-right
message2 = '{"method": "add", "params":["moveright", "moveright", "this documents moveright"], "id": 2}'
print(message2)
received = rpc_interface.communicate_socket(move_socket, message2)
print(f"received: {received}")




while not quit:
    if instructions:
        display_instructions(screen)

    else:
        if level_done:
            display_intertrial_screen(screen)
        else:
            display_intertrial_screen_after_crash(screen)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if instructions:
                    practice_trial = practice_list_of_attempt_dict_keys[0]
                    level_done = run_visualization(surface=screen, scaling=scaling, tiny_visualization=False, FPS=FPS,
                                                   keyboard_input=True,
                                                   obstacles_lists_file=f'object_list_{practice_trial[0]}.csv',
                                                   drift_ranges_file=f'drift_ranges_{practice_trial[0]}.csv',
                                                   wall_list_file=f'walls_dict_{practice_trial[0]}.csv',
                                                   input_noise_magnitude=practice_trial[2],
                                                   input_noise_threshold=0,
                                                   drift_enabled=practice_trial[1],
                                                   trial=practice_trial[0],
                                                   attempt=practice_attempt_dict[practice_trial]+1,
                                                   n_run=n_run, code=code)
                    if level_done:
                        practice_list_of_attempt_dict_keys.remove(practice_trial)
                    if len(practice_list_of_attempt_dict_keys) < 1:
                        instructions = False
                else:
                    random.shuffle(list_of_attempt_dict_keys)
                    trial = list_of_attempt_dict_keys[0]

                    level_done = run_visualization(surface=screen, scaling=scaling, tiny_visualization=False, FPS=FPS,
                                                   keyboard_input=True,
                                                   obstacles_lists_file=f'object_list_{trial[0]}.csv',
                                                   drift_ranges_file=f'drift_ranges_{trial[0]}.csv',
                                                   wall_list_file=f'walls_dict_{trial[0]}.csv',
                                                   input_noise_magnitude=trial[2],
                                                   drift_enabled=trial[1],
                                                   trial=trial[0],
                                                   attempt=attempt_dict[trial]+1,
                                                   n_run=n_run, code=code)
                    n_run += 1
                    attempt_dict[trial] += 1

                    if level_done:  # if level was successfully solved, it won't be played again
                        list_of_attempt_dict_keys.remove(trial)
                    else:
                        if attempt_dict[trial] >= max_attempts:  # if max_attempts reached, level won't be played again
                            list_of_attempt_dict_keys.remove(trial)

                    if len(list_of_attempt_dict_keys) < 1:  # if no level are left to play -> quit
                        quit = True

# print(attempt_dict)
pygame.quit()
