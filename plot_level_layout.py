import matplotlib.pyplot as plt
import numpy as np
from helper_functions import get_wall_positions, get_player_positions, get_obstacles_lists, get_drift_ranges
from config import scaling, level_size_x


def plot_level_layout(trial=1, safe_plot=False):

    wall_list_file = f'walls_dict_{trial}.csv'
    wall_list = get_wall_positions(wall_list_file)

    level_size_y = len(wall_list)

    obstacles_lists_file = f'object_list_{trial}.csv'
    obstacles_list, flag_multiple_obstacle_lists = get_obstacles_lists(obstacles_lists_file)

    drift_ranges_file = f'drift_ranges_{trial}.csv'
    drift_ranges = get_drift_ranges(drift_ranges_file)

    fig, ax = plt.subplots(figsize=(5, 12), dpi=80)

    plt.rcParams.update({'font.size': 16})
    # plt.tick_params(
    #     axis='y',  # changes apply to the x-axis
    #     which='both',  # both major and minor ticks are affected
    #     left=False,  # ticks along the bottom edge are off
    #     labelleft=False)  # labels along the bottom edge are off
    plt.tick_params(
        axis='y',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        labelsize=16)  # labels along the bottom edge are off

    plt.tick_params(
        axis='x',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        labelsize=16)  # labels along the bottom edge are off

    ax.set_title('level setup')
    ax.set_xlim(-10, level_size_x+10)
    ax.set_xticks(np.arange(0, 41, step=40))
    # ax.set_xticklabels(['0', '360', '720'], fontsize=12)

    ax.set_ylim(0, level_size_y)
    ax.set_yticks(np.arange(0, level_size_y+1, step=level_size_y/20))
    # ax.set_yticklabels(['0', '4500', '9000'], fontsize=12)

    for key in obstacles_list:
        plt.plot(key['x'], key['y'], color='green', marker='o', markersize=key['size'])  # arguments in Comet(): x-pos, y-pos, tile_size

    for i in range(1, len(wall_list) + 1):
        # left wall
        left_wall_x_pos = (wall_list[str(i)][0])
        ax.plot(left_wall_x_pos, i, color='black', marker='s', markersize=1)
        # i*scaling will result in the correct y-coord of the wall

        # right wall
        right_wall_x_pos = (wall_list[str(i)][1])
        ax.plot(right_wall_x_pos, i, color='black', marker='s', markersize=1)

    for drift_info in drift_ranges:
        # drift of any magnitude to the left (negative drift value) is displayed right outside of the right side of
        # the level and vice versa
        for i in range(drift_info[0], drift_info[1]+1):
            drift_pos = 1 if drift_info[2] > 0 else -1
            ax.plot(20 + drift_pos*(-24), i, color='red', marker='s', markersize=1)

    # scale and invert axes
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    ax.invert_yaxis()

    # add time axis
    # conversion functions
    y_to_t = lambda step: step*0.05 + 0.7
    t_to_y = lambda t_: t_/0.05 - 0.7

    sec_y_axis = ax.secondary_yaxis('right', functions=(y_to_t, t_to_y))
    sec_y_axis.set_ylabel('time in seconds', size=22)
    sec_y_axis.invert_yaxis()

    # plt.grid(True)
    if safe_plot:
        plt.savefig(f'complete_design_level_{trial}.png')
    plt.show()
