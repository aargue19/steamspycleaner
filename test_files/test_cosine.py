import pandas as pd
import numpy as np
from scipy import spatial







#########################################################################
# BELOW IS THE CALCULATION OF COSINE SIMILARITY

df = pd.read_csv("step5_result.csv",index_col=False)
df = df.replace(999999,np.nan)
df = df.replace(np.nan,0)

df = df.loc[(df.genre_1 != 'Animation & Modeling')
            & (df.genre_1 != 'Audio Production') 
            & (df.genre_1 != 'Video Production')
            & (df.genre_1 != 'Education')
            & (df.genre_1 != 'Free to Play') , :]

columns = [2,31] + list(np.arange(37,463))

t0_tags_df = df.iloc[:,columns]

# Change all null cells to 0 and all positive cells to 1
#t0_tags_df.iloc[:,2:len(t0_tags_df.columns)] = t0_tags_df.mask(t0_tags_df.iloc[:,2:len(t0_tags_df.columns)]>=1, 1)
# print(t0_tags_df.iloc[0:6,0:6])

t0_tags_df = t0_tags_df.loc[t0_tags_df.genre_1=="Action"]

how_many_action_games = len(t0_tags_df)

# print(f"{how_many_action_games} action games")
 
t0_tags_df = t0_tags_df.iloc[:,2:len(t0_tags_df.columns)-1]  

# print(t0_tags_df.iloc[1:10,0:6])

t0_tags_df = t0_tags_df.mask(t0_tags_df >=1, 1)

t0_tags_df.to_csv("test2222.csv")

action_prototype_df = t0_tags_df.apply(lambda x: x.sum(), axis='rows')

action_prototype_df = action_prototype_df / how_many_action_games
# print(list_of_counts.head())
# print(len(list_of_counts))

action_prototype_list = action_prototype_df.tolist()
# print(action_tags_prototype)

action_prototype_df = pd.DataFrame({"code" : action_prototype_df.index, "count" : action_prototype_df})

# print(action_prototype_df.head)
# print(action_prototype_df.columns)

# APPLY TAG NAMES AND CHECK OUt THE WEIGHTS OF THE PROTOTYPE

tag_codes_df = pd.read_csv("tag_codes.csv")

# print(tag_codes_df.head)

for i in range(len(tag_codes_df)):
    tag_codes_df.code[i] = f"tag_{tag_codes_df.code[i]}"

#print(tag_codes_df.head)

prototype_mgd_df = pd.merge(action_prototype_df,tag_codes_df, on='code')
prototype_mgd_df = prototype_mgd_df.sort_values(by=['count'], ascending=False)
#print(prototype_mgd_df.iloc[0:10])

# CHECK OUT THE NAMES OF THE TAGS FOR THE FIRST GAME

example_game = t0_tags_df.iloc[3,:]

example_game_df = pd.DataFrame({"code" : example_game.index, "tag_count" : example_game})

mgd_df = pd.merge(example_game_df,tag_codes_df, on='code')

# print(example_game_df.loc[example_game_df.tag_count == 1])

mgd_df = mgd_df.sort_values(by=['tag_count'], ascending=False)

print(mgd_df.iloc[0:20,:])


#############################################################################################
# CALCULATE THE COSINE SIMILARITY OF A COUPLE GAMES

# print(df.head)S

first_game = t0_tags_df.iloc[3,:].tolist()
second_game = t0_tags_df.iloc[99,:].tolist()

# print(len(first_game))
# print(first_game)

# print(len(second_game))
# print(second_game)

# print(len(action_tags_prototype))
# print(action_tags_prototype)

# first_game_df = t0_tags_df.iloc[0,:]
# first_game_df = first_game_df[first_game_df != 0]

#print(first_game_df)

result1 = 1 - spatial.distance.cosine(first_game, action_prototype_list)

print(f"similarity of first game and prototype: {result1}")

# print(len(second_game))
# print(len(action_tags_prototype))

# second_game_df = t0_tags_df.iloc[1,:]
# second_game_df = second_game_df[second_game_df != 0]

# print(second_game_df)

# result2 = 1 - spatial.distance.cosine(second_game, action_tags_prototype)

# print(f"similarity of second game and prototype: {result2}")

