#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 19 07:37:22 2020

@author: tom
"""


'''
--------------------------> SET UP ENVIRONMENT
'''

import pandas as pd #dataframes
import matplotlib.pyplot as plt #plotting function


'''
--------------------------> PREPARE DATA
'''



#load data
df = pd.read_csv("data/solo.csv") #import
len(df['player_id'].unique()) #Sanity check: how many players do we have? n = 2105

#tidy data
df['time_end']=pd.to_datetime(df['time_end']) #convert to datetime object so time of game is explicitly coded

#add game number
df['game_n']=df.groupby('player_id')['time_end'].rank(ascending=True)
df['game_n']=df['game_n'].astype(int) #force integer values only 


#sanity check: look at one player and line up by time of game and check game n tracks this
df[df['player_id']==114].sort_values(by='time_end')



'''
--------------------------> MAKE PLOTS
'''



plt.clf()
#find max game per plays
df.groupby('player_id')['game_n'].max().hist() #note that this shows we filtered our original data by people who played at least 100 games
plt.title('Distribution of total number of games by player')
plt.xlabel('Total number of games')
plt.ylabel('Frequency')
plt.savefig('plots/dist_games.png',bbox_inches='tight')

max_games=50 #limit for our x-axis
plt.clf()
#plot game n vs average score, using median to account for outliers

y=df[df['game_n']<=max_games].groupby('game_n')['mean'].median().values
x=df[df['game_n']<=max_games].groupby('game_n')['mean'].median().index
#interquartile range
yerr=df[df['game_n']<=max_games].groupby('game_n')['mean'].quantile(0.75).values-df[df['game_n']<=max_games].groupby('game_n')['mean'].quantile(0.25).values
plt.plot(x,y,'.',ms=15)
plt.ylabel('Median score')
plt.xlabel('Game number')
plt.title('Score against practice')
plt.savefig('plots/lcurve_wo_errors.png',bbox_inches='tight')
plt.errorbar(x,y,yerr)
plt.ylabel('Median score (interquartile range')
plt.savefig('plots/lcurve_w_errors.png',bbox_inches='tight')