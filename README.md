# Skill acquisition of solo players: a case study 

## `Coursework for PSY6422` (yidan)


In this project, I leverage the research data of [Landfried et al. (2019)](https://doi.org/10.1371/journal.pone.0211014), which is collected from the game *Conquer Club*.
While they mainly focus on **teamwork**'s effect on skill acquisition, I think a baseline which only consists of solo player's performance should be considered.
To justify the (early) learning pattern of solo players, in [the first notebook](/filter.ipynb) I filter the data of the palyers who **have never palyed with a teammate**.
Next, in [the second notebook](./visualisation.ipynb) I visualise and analyse the filtered data.

## Tom's notes

Landfried, G., Slezak, D. F., & Mocskos, E. (2019). Faithfulness-boost effect: Loyal teammate selection correlates with skill acquisition improvement in online games. PloS one, 14(3), e0211014. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0211014
- "The problem of skill acquisition is ubiquitous and fundamental to life. Most tasks in modern society involve the cooperation with other subjects. Notwithstanding its fundamental importance, teammate selection is commonly overlooked when studying learning. We exploit the virtually infinite repository of human behavior available in Internet to study a relevant topic in anthropological science: how grouping strategies may affect learning. We analyze the impact of team play strategies in skill acquisition using a turn-based game where players can participate individually or in teams. We unveil a subtle but strong effect in skill acquisition based on the way teams are formed and maintained during time. “Faithfulness-boost effect” provides a skill boost during the first games that would only be acquired after thousands of games. The tendency to play games in teams is associated with a long-run skill improvement while playing loyally with the same teammate significantly accelerates short-run skill acquisition."




#get data
https://datadryad.org/stash/dataset/doi:10.5061/dryad.888gm50

#decompress
tar -xvf 308893369.tar.gz 

#join
cat xaa xab xac xad xae xaf xag xah > gamesdb.gz
#unpack
gunzip gamesdb.gz

#install postgres
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04

sudo apt-get install postgresql postgresql-contrib

#create role and db which match linux user nam ('tom')

#import

sudo -u tom psql tom < gamesdb

#export from sql csv

#from interactive postgres serve
tom=# \copy public.play (player_id, game_id, time_end, team, mean, std) TO 'temp.csv' CSV HEADER

