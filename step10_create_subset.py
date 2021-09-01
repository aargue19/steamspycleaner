import pandas as pd
import numpy as np

df = pd.read_csv("step9_result.csv", low_memory=False)

# cols = df.columns.tolist()
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")

# #FIRST REMOVE GAMES THAT WERE IN EARLY ACCESS AT ANY POINT

df.iloc[:,113:538] = df.iloc[:,113:538].replace(np.nan, 0)
df.iloc[:,540:965] = df.iloc[:,540:965].replace(np.nan, 0)
df.iloc[:,113:538] = df.iloc[:,113:538].replace(999999, 0)
df.iloc[:,540:965] = df.iloc[:,540:965].replace(999999, 0)

#LOAD THE LIST OF EX EARLY ACCESS GAMES AND REMOVE THEM FROM THE DATAFRAME
ex_ea_games = pd.read_csv("./raw_data/ex_early_access_games.csv")
ex_ea_names_list = ex_ea_games['Game'].tolist()
df = df.loc[~df["app_name_x"].isin(ex_ea_names_list)]

print(len(df))

# REMOVE ANY GAMES WITH THE EARLY ACCESS TAG AT T1 (TAG #493)

df.tag_493 = df.tag_493.astype(int)
df = df.loc[~(df['tag_493'] > 0)]
print(len(df))

# DOUBLE CHECK THE TAG COUNTS SCRAPED FROM STEAMSPY FOR ANY REMAINING EA GAMES

for i in range(1,21):
    current_col = f'tag_{i}_scrap'
    if len(df.loc[df[current_col] == "Early+Access"]) >0:
        df = df.loc[~(df[current_col] == "Early+Access")]

print(len(df))

#REMOVE UNWANTED GENRES LIKE UTILITIES

# print(set(df.genre_1.tolist()))
# {nan, 'RPG', 'Audio Production', 'Action', 'Design & Illustration', 'Violent', 'Simulation', 'Adventure', 'Animation & Modeling', 
# 'Web Publishing', 'Strategy', 'Video Production', 'Racing', 'Sports', 'Indie', 'Free to Play', 'Utilities', 'Casual'}

for i in range(1,11):

    df = df.loc[~((df[f'genre_{i}'] == 'Audio Production') | 
                (df[f'genre_{i}'] == 'Design & Illustration') |
                (df[f'genre_{i}'] == 'Animation & Modeling') |
                (df[f'genre_{i}'] == 'Web Publishing') |
                (df[f'genre_{i}'] == 'Video Production') |
                (df[f'genre_{i}'] == 'Utilities') |
                (df[f'genre_{i}'] == 'Education')]



print(len(df))             

df.to_csv("step10_result.csv")










# print(df.iloc[:,0:22].dtypes)
# print(df.iloc[:,540:550].dtypes)

# df.infer_objects()

# print(df.iloc[:,0:22].dtypes)
# print(df.iloc[:,540:550].dtypes)


# df.infer_objects()

# # using dictionary to convert specific columns
# convert_dict = {'': int,
#                 'C': float
#                }

# df = df.astype(convert_dict)
# print(df.dtypes)








# id, genres 1-10, t1 tags
# test_range = np.r_[2, 32:42, 113:538]



# cols = df.columns.tolist()

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")


# df = df.iloc[np.r_[2:3, 25:28]]

# df = df.iloc[:,2:]


