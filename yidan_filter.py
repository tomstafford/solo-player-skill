#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 16:16:16 2020

Yidan's notebook

Export original database

The original data is stored in a huge PostgreSQL textual dump. After configuring the database, I embed my a SQL query into an export command: .\psql.exe copy public.play (player_id, game_id, time_end, team, mean, std) TO play_data.csv CSV HEADER ENCODING 'UTF8' QUOTE '\"' ESCAPE '''';

The meaning of some important entries:

    player_id & game_id: global identifiers of players & games
    team: team id (of a particular game)
    mean & std: statistics of skills

The exported table is still quite large (2 GB). Please access Google Drive to download it. Using my PC, I cannot process this table as a R dataframe. As a result, I turn to Python to read & filter the data.
Filter

My pipeline contains three steps:

    find the game_ids which have multi-player teams;
    find solo players who never enter these games;
    find the solo players who have at least MIN_FREQ records.

"""



# step 1
def group_game_finder(table_path):
    game_team_set = set()
    group_game_set = set()

    target_file = open(table_path, "r")
    header = target_file.readline()
    line = target_file.readline().strip().split(",")
    while len(line) > 2:
        game_id = int(line[1])
        team = int(line[3])

        if (game_id, team) in game_team_set:  # in at least one team, there are two players
            group_game_set.add(game_id)
        game_team_set.add((game_id, team))

        line = target_file.readline().strip().split(",")

    target_file.close()
    return group_game_set




# step 2
def solo_player_finder(table_path, group_game_set):
    team_player_set = set()
    all_player_set = set()

    target_file = open(table_path, "r")
    header = target_file.readline()
    line = target_file.readline().strip().split(",")
    while len(line) > 2:
        player_id = int(line[0])
        game_id = int(line[1])

        all_player_set.add(player_id)
        if game_id in group_game_set:
            team_player_set.add(player_id) # have played in a "group game" for at least once

        line = target_file.readline().strip().split(",")

    target_file.close()
    return all_player_set - team_player_set

# excute step 1&2
original_table_path = "play_data.csv"

MIN_FREQ = 100

solo_player_set = solo_player_finder(original_table_path, group_game_finder(original_table_path))

# step 3
target_file = open(original_table_path, "r")
filtered_file = open("solo.csv", "w")
filtered_file.write(target_file.readline())

line = target_file.readline()
solo_dict = {}
while len(line) > 2:
    player_id = int(line.strip().split(",")[0])
    
    # *complete (not N/A)* records of solo players  
    if player_id in solo_player_set and min(map(len, map(str.strip, line.split(",")))) > 0:  
        solo_dict.setdefault(player_id, set())
        solo_dict[player_id].add(line)
    line = target_file.readline()

num = 0
for item in solo_dict:
    if 250 > len(solo_dict[item]) >= MIN_FREQ:  # why 250: I observe one outlier player who have played over 250 solo games!
        num += 1
        for line in solo_dict[item]:
            filtered_file.write(line)

target_file.close()
filtered_file.close()
<<<<<<< HEAD
=======

# 1013582 rows
>>>>>>> 88f9ed422e3b1e5a9c4f837e7421f1d66d348ca4
