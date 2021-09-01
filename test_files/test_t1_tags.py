import pandas as pd
import numpy as np

#EXCLUDE GAMES WHERE THE TAGS DATA CAME AFTER THE RELEASE DATE

df = pd.read_csv("step5_result.csv")

# convert the 'Date' column to datetime format
df['release_date']= pd.to_datetime(df['release_date'])
df['tag_date']= pd.to_datetime(df['tag_date'])

#print(df.loc[:,['app_name','release_date','tag_date']].dtypes)

list_of_ids = df['app_id'].tolist()
list_of_ids = set(list_of_ids)
list_of_ids = list(list_of_ids)

#CREATE A COLUMN TO INDICATE IF A ROW IS THE EARLIEST TAGS FOR EACH GAME

df['tag_before_release'] = np.where(df['release_date']>df['tag_date'], "yes", "no")

df['days_btw_release_first_tags'] = ((df.tag_date - df.release_date)/np.timedelta64(1, 'D'))
df['days_btw_release_first_tags'] = df['days_btw_release_first_tags'].astype(int)

full_df2 = pd.DataFrame(columns=df.columns)

ids_to_check = list(set(df['app_id'].tolist()))

counter = 0

problems = []

for current_id in ids_to_check:

    try:
        current_idx = df['days_btw_release_first_tags'].loc[df['app_id'] == current_id].idxmin()

        temp_df = df.loc[df.index == current_idx,:]

        full_df2 = pd.concat([full_df2, temp_df], ignore_index=True, sort=False)
    
        print(counter)
        counter+=1

    except Exception as e:
        print(current_id)
        problems.append(current_id)
        print(e)

full_df2.to_csv("test2222.csv")

print(problems)







# #CREATE A COLUMN TO INDICATE IF A ROW IS THE FIRST TAGS AFTER THE ONE YEAR MARK FOR EACH GAME



# # df['tag_before_release'] = np.where(df['release_date']>df['tag_date'], "yes", "no")

# #MAKE A SUBSET OF JUST THE EARIEST RECORD OF TAGS

# games_with_producer_tags = []

# for current_id in list_of_ids:
#     if "yes" in set(df['tag_before_release'].loc[df.app_id == current_id]):
#         games_with_producer_tags.append(current_id)

# tags_before_release_df = df[df["app_id"].isin(games_with_producer_tags)]

# # print(len(set(games_with_producer_tags)))

# #use just the first game in the list to set up the dataframe
# current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == games_with_producer_tags[0]].idxmin()

# full_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

# #iterate through and append the rest of the games
# for current_id in games_with_producer_tags[1:len(games_with_producer_tags)]:

#     try:
#         current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == current_id].idxmin()

#         temp_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

#         full_df = pd.concat([full_df, temp_df], ignore_index=True, sort=False)
    
#     except Exception as e:
#         print(current_id)
#         break


# #EXCLUDE COLUMN # 444 WHICH iS THE GAME_BEFORE_RELEASE COL

# # xxxx = []
# # for cnum in range(len(cols)):
# #     xxxx.append([cnum,cols[cnum]])
# # print(xxxx)
# # print(len(cols))
# # print("\n")
# # print("\n")

# cols = full_df.columns.tolist()
# myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,438]
# myorder = myorder + list(np.arange(13,438,1)) + [439,440]
# mylist = [cols[i] for i in myorder]
# full_df = full_df[mylist]

# # xxxx = []
# # for cnum in range(len(cols)):
# #     xxxx.append([cnum,cols[cnum]])
# # print(xxxx)
# # print(len(cols))

# full_df.to_csv("step6_tags_t1.csv",index=False)