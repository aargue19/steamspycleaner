# STEP 1 - GET TAG CODES

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# "steamdb_tag_codes_raw.txt" is the raw source from the page "view-source:https://steamdb.info/tags/"

# HERE I PARSE THE HTML TO GET THE TAG NAME, TAG CODE AND COUNT

with open('~/raw/data/steamdb_tag_codes_raw.txt') as f:
    read_data = f.read()
    page_content = BeautifulSoup(read_data, "html.parser")

list_of_links = page_content.find_all("a", {"class": "label-link"}, href=True)

list_of_codes = []

for lnk in list_of_links:
    list_of_codes.append(re.findall("(?<=tag/)(.*)(?=/ )", str(lnk))[0])

list_of_counts = page_content.find_all("span", {"class": "label-count"})

list_of_counts_clean = []

for cnt in list_of_counts:
    list_of_counts_clean.append(re.findall('(?<=\<span class="label-count flex-grow muted">)(.*)(?= products)', str(cnt))[0])

all_rows=[]

for i in range(len(list_of_links)):
    current_row = [list_of_codes[i], list_of_links[i].text, list_of_counts_clean[i]]
    all_rows.append(current_row)

df = pd.DataFrame(all_rows, columns = ['tag_code', 'tag_name', 'tag_count'])
    
df.to_csv("~/raw_data/tag_names_codes_counts.csv", index=False)

# STEP 2 - GET GAME IDS

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# "raw_steamspy_year_2017.txt" is the raw source from the page "view-source:https://steamspy.com/year/2017"
# I DID A FIND/REPLACE ON <td data-order=""> to GET RID OF ANY BLANK NAMES OF GAMES OR DEVS (CHANGED TO XXXXXX)    #### YOU SHOULD CODE THIS SO YOU DONT HAVE TO DO IT MANUALLY
## YOU SHOULD ALSO INCLUDE SOME CODE TO REMOVE THE RECORDS WHERE YOU REPLACED BLANK ENTRIES  ("XXXXXX") BEFORE WRITING TO FILE

## ALSO SHOULD DO A REPLACE "N/A" AND "Free" WITH ZEROS IN PRICE_DECIMAL COLUMN BEFORE WRITING TO FILE


with open('~/raw_data/steamspy_year_2017_games_raw.txt', encoding="utf8") as f:
    read_data = f.read()
    page_content = BeautifulSoup(read_data, "html.parser")


# PARSE THE HTML TO GET THE GAME NAMES
list_of_names=[]

# test_string = '<td data-order="Dungeon's Barrage">'
# print(re.findall("(?<=data-order=")(.*)(?=")))")

list_of_tds = page_content.find_all("td")

for td in list_of_tds:
    list_of_names.append(re.findall('(?<=data-order=")(.*)(?="><a)', str(td)))

good_names = []

for name in list_of_names:
    if len(name) > 0:
        good_names.append(name)

#print(len(good_names))

# PARSE THE HTML TO GET THE APP ID
list_of_ids = []

# test_string = '/app/434460'
# print(re.findall("(?<=app\/)(.*)", test_string))

list_of_links = page_content.find_all("a", href=True)

for lnk in list_of_links:
    list_of_ids.append(re.findall("(?<=app\/)(.*)", str(lnk['href'])))

# print(list_of_ids)

good_ids =[]

for i in list_of_ids:
    if len(i) > 0:
        good_ids.append(i)


# GET RELEASE DATES

list_of_rel_tds = page_content.find_all("td", {"class":"treleasedate"})

list_of_dates = []

for td in list_of_rel_tds:
    list_of_dates.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))

#GET PRICES 

list_of_price_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices = []

for td in list_of_price_tds:
    list_of_prices.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))



#GET PRICES WITH DECIMALS AND $

list_of_price_dec_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices_dec = []

for td in list_of_price_dec_tds:
    
    list_of_prices_dec.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# GET user_score_meta_score
#<td class="tuserscore" data-order="0">N/A (N/A/62%)</td>

list_of_score_tds = page_content.find_all("td", {"class":"tuserscore"})

list_of_scores = []

for td in list_of_score_tds:
    
    list_of_scores.append(re.findall('(?<=">)(.*)(?=<)', str(td)))



# GET OWNERS

# BE CAREFUL B/C FOR SOME REASON THE </FONT> TAG DISAPPEARS

# test_string = '<td data-order="100,000">100,000&nbsp;..&nbsp;200,000</font></td>'
# print(re.findall('(?=td data-order=\"\d)(.*)(?=<)',test_string))

#<td data-order="200,000">200,000&nbsp;..&nbsp;500,000</font></td>
list_of_owners = []

list_of_no_class_tds = page_content.find_all("td",{'class': None})

for td in list_of_no_class_tds[2::5]:
    list_of_owners.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

# print(list_of_owners[0:20])
# print(len(list_of_owners))



# print(list_of_owners_clean[0:10])
# print(len(list_of_owners_clean))

# GET PLAYTIME

list_of_ptimes = []
list_of_ptime_tds = page_content.find_all("td",{"class": "tplaytime"})

for td in list_of_ptime_tds:
    
    list_of_ptimes.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# print(list_of_ptimes[0:10])
# print(len(list_of_ptimes))


# GET DEVELOPER 

list_of_blank_tds = []
list_of_tds = page_content.find_all("td",{"class": None})

d1=[]
d2=[]

for td in list_of_tds[3::5]:
    d1.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

for td in list_of_tds[4::5]:
    d2.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))


# CHECK LENGTHS 
# print(len(good_names))
# print(len(good_ids))
# print(len(list_of_dates))
# print(len(list_of_prices))
# print(len(list_of_prices_dec))
# print(len(list_of_owners)) #######
# print(len(list_of_scores))
# print(len(list_of_ptimes))
# print(len(d1))
# print(len(d2))

# PREPARE ROWS FOR DF
all_rows=[]

for i in range(len(good_ids)):
    current_row = [i, good_names[i][0], good_ids[i][0], list_of_dates[i][0], list_of_prices[i][0], list_of_prices_dec[i][0],
                   list_of_scores[i][0], list_of_owners[i][0], list_of_ptimes[i][0], d1[i][0], d1[i][0], d2[i][0], d2[i][0]]
    all_rows.append(current_row)

# CREATE DF AND WRITE TO FILE
# colnames: app_num,app_name,app_id,release_date,price,price_decimal,user_score_meta_score,owners,playtime_median,developer,developer2,publisher,publisher2

df = pd.DataFrame(all_rows, columns = ['app_num', 'app_name', 'app_id','release_date','price','price_decimal',
                                       'user_score_meta_score','owners','playtime_median','developer','developer2', 'publisher', 'publisher2'])

df.to_csv("~/raw_data/steamspy_games_clean.csv", index=False)

# STEP 3 - SCRAPE CSVS

import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

# "raw_steamspy_year_2017.txt" is the raw source from the page "view-source:https://steamspy.com/year/2017"
# I DID A FIND/REPLACE ON <td data-order=""> to GET RID OF ANY BLANK NAMES OF GAMES OR DEVS (CHANGED TO XXXXXX)    #### YOU SHOULD CODE THIS SO YOU DONT HAVE TO DO IT MANUALLY
## YOU SHOULD ALSO INCLUDE SOME CODE TO REMOVE THE RECORDS WHERE YOU REPLACED BLANK ENTRIES  ("XXXXXX") BEFORE WRITING TO FILE

## ALSO SHOULD DO A REPLACE "N/A" AND "Free" WITH ZEROS IN PRICE_DECIMAL COLUMN BEFORE WRITING TO FILE


with open('~/raw_data/steamspy_year_2017_games_raw.txt', encoding="utf8") as f:
    read_data = f.read()
    page_content = BeautifulSoup(read_data, "html.parser")


# PARSE THE HTML TO GET THE GAME NAMES
list_of_names=[]

# test_string = '<td data-order="Dungeon's Barrage">'
# print(re.findall("(?<=data-order=")(.*)(?=")))")

list_of_tds = page_content.find_all("td")

for td in list_of_tds:
    list_of_names.append(re.findall('(?<=data-order=")(.*)(?="><a)', str(td)))

good_names = []

for name in list_of_names:
    if len(name) > 0:
        good_names.append(name)

#print(len(good_names))

# PARSE THE HTML TO GET THE APP ID
list_of_ids = []

# test_string = '/app/434460'
# print(re.findall("(?<=app\/)(.*)", test_string))

list_of_links = page_content.find_all("a", href=True)

for lnk in list_of_links:
    list_of_ids.append(re.findall("(?<=app\/)(.*)", str(lnk['href'])))

# print(list_of_ids)

good_ids =[]

for i in list_of_ids:
    if len(i) > 0:
        good_ids.append(i)


# GET RELEASE DATES

list_of_rel_tds = page_content.find_all("td", {"class":"treleasedate"})

list_of_dates = []

for td in list_of_rel_tds:
    list_of_dates.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))

#GET PRICES 

list_of_price_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices = []

for td in list_of_price_tds:
    list_of_prices.append(re.findall('(?<=data-order=")(.*)(?=">)', str(td)))



#GET PRICES WITH DECIMALS AND $

list_of_price_dec_tds = page_content.find_all("td", {"class":"tprice"})

list_of_prices_dec = []

for td in list_of_price_dec_tds:
    
    list_of_prices_dec.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# GET user_score_meta_score
#<td class="tuserscore" data-order="0">N/A (N/A/62%)</td>

list_of_score_tds = page_content.find_all("td", {"class":"tuserscore"})

list_of_scores = []

for td in list_of_score_tds:
    
    list_of_scores.append(re.findall('(?<=">)(.*)(?=<)', str(td)))



# GET OWNERS

# BE CAREFUL B/C FOR SOME REASON THE </FONT> TAG DISAPPEARS

# test_string = '<td data-order="100,000">100,000&nbsp;..&nbsp;200,000</font></td>'
# print(re.findall('(?=td data-order=\"\d)(.*)(?=<)',test_string))

#<td data-order="200,000">200,000&nbsp;..&nbsp;500,000</font></td>
list_of_owners = []

list_of_no_class_tds = page_content.find_all("td",{'class': None})

for td in list_of_no_class_tds[2::5]:
    list_of_owners.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

# print(list_of_owners[0:20])
# print(len(list_of_owners))



# print(list_of_owners_clean[0:10])
# print(len(list_of_owners_clean))

# GET PLAYTIME

list_of_ptimes = []
list_of_ptime_tds = page_content.find_all("td",{"class": "tplaytime"})

for td in list_of_ptime_tds:
    
    list_of_ptimes.append(re.findall('(?<=">)(.*)(?=<)', str(td)))

# print(list_of_ptimes[0:10])
# print(len(list_of_ptimes))


# GET DEVELOPER 

list_of_blank_tds = []
list_of_tds = page_content.find_all("td",{"class": None})

d1=[]
d2=[]

for td in list_of_tds[3::5]:
    d1.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))

for td in list_of_tds[4::5]:
    d2.append(re.findall(r'(?<=data-order=")(.*)(?=">)', str(td)))


# CHECK LENGTHS 
# print(len(good_names))
# print(len(good_ids))
# print(len(list_of_dates))
# print(len(list_of_prices))
# print(len(list_of_prices_dec))
# print(len(list_of_owners)) #######
# print(len(list_of_scores))
# print(len(list_of_ptimes))
# print(len(d1))
# print(len(d2))

# PREPARE ROWS FOR DF
all_rows=[]

for i in range(len(good_ids)):
    current_row = [i, good_names[i][0], good_ids[i][0], list_of_dates[i][0], list_of_prices[i][0], list_of_prices_dec[i][0],
                   list_of_scores[i][0], list_of_owners[i][0], list_of_ptimes[i][0], d1[i][0], d1[i][0], d2[i][0], d2[i][0]]
    all_rows.append(current_row)

# CREATE DF AND WRITE TO FILE
# colnames: app_num,app_name,app_id,release_date,price,price_decimal,user_score_meta_score,owners,playtime_median,developer,developer2,publisher,publisher2

df = pd.DataFrame(all_rows, columns = ['app_num', 'app_name', 'app_id','release_date','price','price_decimal',
                                       'user_score_meta_score','owners','playtime_median','developer','developer2', 'publisher', 'publisher2'])

df.to_csv("~/raw_data/steamspy_games_clean.csv", index=False)

#STEP 4 - REMOVE EMPTY CSVS

import pandas as pd
import numpy as np
import os
import datetime
from os import listdir
from os import getcwd

#GET A LIST OF ALL THE CSV FILES WITH TAGS OVER TIME DATA DOWNLOADED FROM STEAMSPY AND CLEAN UP

rootdir = getcwd()

#filepath = rootdir + os.sep + "csvs" + os.sep
filepath = rootdir + os.sep + "csvs" + os.sep
fail_folder_destination = rootdir + os.sep + "empty_csvs" + os.sep

list_of_gamez = []
list_of_file_names = []

with os.scandir(filepath) as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        list_of_file_names.append(entry)
        list_of_gamez.append(entry.name.replace("_",":").replace(".csv",""))

for i in range(1,len(list_of_gamez)):

    try:
        #print(f"trying {list_of_gamez[i]}")

        data = pd.read_csv(list_of_file_names[i])

        column_name_list = data.columns.tolist()

        # print(column_name_list)
        # print(len(column_name_list))

        # if len(column_name_list) < 2 :
        #     print(f"{list_of_gamez[i]}: {len(column_name_list)}") 
    except Exception as e:
        print(f"{list_of_gamez[i]} is empty")

        current_filename = filepath + list_of_file_names[i].name
        current_destination_filename = fail_folder_destination + list_of_file_names[i].name
        print(f"moving file from here: {current_filename}, to here {current_destination_filename}")

        os.rename(current_filename, current_destination_filename)

        ##ADD CODE HERE TO DELETE THESE FILES FROM ORIGINAL DIRECTORY?

# STEP 5 - MERGE CSVS

import pandas as pd
import numpy as np
import os
import datetime
from os import listdir
from os import getcwd

# THE DATA FOR "tag_names_codes_counts.csv" COMES FROM "https://steamdb.info/tags/"
# I SAVED THE RAW SOURCE AS "steamdb_tag_codes_raw.txt"
# I used "step0_get_tag_codes.py" to make "tag_names_codes_counts.csv" which is a list of ALL CODES+totals FOR ALL TAGS

#MAKE A LIST OF ALL THE TAG CODES ON STEAM AND RENAME THEM TO "TAG_####"
tag_codes = pd.read_csv("./raw_data/tag_names_codes_counts.csv")

tag_code_list = tag_codes['tag_code'].tolist()

renamed_tag_code_list = []

for entry in tag_code_list:
    renamed_tag_code_list.append(f"tag_{entry}")

#GET A LIST OF ALL THE CSV FILES WITH TAGS OVER TIME DATA DOWNLOADED FROM STEAMSPY AND CLEAN UP

rootdir = getcwd()

# filepath = rootdir + os.sep + "csvs_a_to_c" + os.sep                              #### BECAUSE USING PYTHON 32-BIT THIS HAD TO BE SPLIT UP
# filepath = rootdir + os.sep + "csvs_d_to_j" + os.sep
# filepath = rootdir + os.sep + "csvs_k_to_r" + os.sep
# filepath = rootdir + os.sep + "csvs_s_to_z" + os.sep
filepath = rootdir + os.sep + "csvs" + os.sep                                       #### steamspycleaner repo venv uses 64-bit python so do it all at once


list_of_gamez = []
list_of_file_names = []

with os.scandir(filepath) as dir_entries:
    for entry in dir_entries:
        info = entry.stat()
        list_of_file_names.append(entry)
        list_of_gamez.append(entry.name.replace("_",":").replace(".csv",""))

#READ THE T.O.T. DATA FROM THE FIRST CSV FILE AND RENAME THE COLUMNS TO "TAG_####", REPLACE MISSING VALUES WITH "999999"

#print(list_of_file_names[0])

data = pd.read_csv(list_of_file_names[0])

column_name_list = data.columns.tolist()

new_column_name_list = []

for colname in column_name_list:
    new_column_name_list.append(f"tag_{colname}")

data.columns = new_column_name_list

data = data.replace(np.nan, 999999)

#data.to_csv("test_step_2.csv")

#CREATE A DATAFRAME WITH COLUMNS FOR ALL 425 THE TAGS AS COLUMNS AND FILL IN TAGS OVER TIME DATA FOR THE CURRENT GAME

df1 = pd.DataFrame(index=np.arange(len(data)), columns = renamed_tag_code_list)

for col_name in data.columns:

    df1[f'{col_name}'] = data[f'{col_name}'].values

df1["app_name"] = list_of_gamez[0]

#MATCH THE RECORDS BASED ON THE APP NAME TO OTHER GAME DETAILS FROM LIST OF ALL GAMES IN THAT YEAR AND APPEND DETAILS OF THE CURRENT GAME TO EACH LINE OF THE DATAFRAME

# df = pd.read_csv('steamspy_2018_games_clean.csv')                                 #THIS IS FOR THE 2018 GAMES
df = pd.read_csv('./raw_data/steamspy_games_clean.csv')
#df = df.loc[~df.app_name.str.contains("<U+"),:]

# #LOAD THE LIST OF EX EARLY ACCESS GAMES AND REMOVE THEM FROM THE DATAFRAME                #### DO THIS AFTER THE WHOLE DATASET IS CREATED (STEP 10?) NOT NOW 
# ex_ea_games = pd.read_csv("./raw_data/ex_early_access_games.csv")
# ex_ea_names_list = ex_ea_games['Game'].tolist()
# df = df.loc[~df["app_name"].isin(ex_ea_names_list)]

line_for_merge = df.loc[df.app_name == list_of_gamez[0],:]

mgd_df = pd.merge(line_for_merge,df1, on="app_name")

#SINCE THIS IS THE FIRST FILE USE IT TO CREATE THE FINAL DF

final_df = mgd_df

#final_df.to_csv("test_2222.csv")

# #DO THE SAME FOR ALL OTHER FILES AND APPEND THEM TO THE FINAL DATAFRAME

for i in range(1,len(list_of_gamez)):

    print(f"trying {list_of_gamez[i]}")

    data = pd.read_csv(list_of_file_names[i])

    column_name_list = data.columns.tolist()

    new_column_name_list = []

    for colname in column_name_list:
        new_column_name_list.append(f"tag_{colname}")

    data.columns = new_column_name_list

    data = data.replace(np.nan, 999999)

    #CREATE A DATAFRAME WITH COLUMNS FOR ALL 425 THE TAGS AS COLUMNS AND FILL IN TAGS OVER TIME DATA FOR THE CURRENT GAME

    df1 = pd.DataFrame(index=np.arange(len(data)), columns = renamed_tag_code_list)

    for col_name in data.columns:

        df1[f'{col_name}'] = data[f'{col_name}'].values

    df1["app_name"] = list_of_gamez[i]

    #LOAD THE FILE WITH 2018 GAME DETAILS AND APPEND DETAILS OF THE CURRENT GAME TO EACH LINE OF THE DATAFRAME

    line_for_merge = df.loc[df.app_name == list_of_gamez[i],:]

    mgd_df = pd.merge(line_for_merge,df1, on="app_name")

    final_df = final_df.append(mgd_df, ignore_index=True)


# THERE ARE SOME WEIRD COLUMNS THAT YOU MAY NEED TO GET RID OF
#ORIGINALLY YOU DID THIS IN STEP 5 BUT YOU SHOULD DO IT HERE IF THEY COME UP

cols_to_drop = ['tag_999999',
                'tag_5144',
                'tag_1694',
                'tag_134316', 
                'tag_9090',
                'tag_1735']

for col_name in cols_to_drop:
    try:
        final_df = final_df.drop(f'{col_name}', 1)
    except Exception as e:
        print(e)


#WHEN FINISHED WRITE TO FILE

# final_df.to_csv("step5_result_a_to_c.csv", index=False)
# final_df.to_csv("step5_result_d_to_j.csv", index=False)
# final_df.to_csv("step5_result_k_to_r.csv", index=False)
# final_df.to_csv("step5_result_s_to_z.csv", index=False)
final_df.to_csv("step5_result.csv", index=False)                #### steamspycleaner repo venv uses 64-bit python so do it all at once

# STEP 6 - GET t1 and t2 tags

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

df['tag_before_release'] = np.where(df['release_date']>=df['tag_date'], "yes", "no")

#CREATE A COLUMN TO INDICATE IF A ROW IS THE FIRST TAGS AFTER THE ONE YEAR MARK FOR EACH GAME



# df['tag_before_release'] = np.where(df['release_date']>df['tag_date'], "yes", "no")

#MAKE A SUBSET OF JUST THE EARIEST RECORD OF TAGS

games_with_producer_tags = []

for current_id in list_of_ids:
    if "yes" in set(df['tag_before_release'].loc[df.app_id == current_id]):
        games_with_producer_tags.append(current_id)

tags_before_release_df = df[df["app_id"].isin(games_with_producer_tags)]

# print(len(set(games_with_producer_tags)))

#use just the first game in the list to set up the dataframe
current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == games_with_producer_tags[0]].idxmin()

full_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

#iterate through and append the rest of the games
for current_id in games_with_producer_tags[1:len(games_with_producer_tags)]:

    try:
        current_idx = tags_before_release_df['tag_date'].loc[tags_before_release_df['app_id'] == current_id].idxmin()

        temp_df = tags_before_release_df.loc[tags_before_release_df.index == current_idx,:]

        full_df = pd.concat([full_df, temp_df], ignore_index=True, sort=False)
    
    except Exception as e:
        print(current_id)
        break


#EXCLUDE COLUMN # 444 WHICH iS THE GAME_BEFORE_RELEASE COL

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")
# print("\n")

cols = full_df.columns.tolist()
myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,438]
myorder = myorder + list(np.arange(13,438,1)) + [439,440]
mylist = [cols[i] for i in myorder]
full_df = full_df[mylist]

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))

full_df.to_csv("step6_tags_t1.csv",index=False)

###########################################################################################################
# GAMES WITH NO TAGS AFTER 6 MONTHS:
# GOOD GIRL (1 MO)

df1 = df

df2 = df1.drop(['tag_before_release'], axis=1)

# df2 = df1.loc[:, df1.columns != 'tag_before_release']

df2 = df2.loc[df2.app_id.isin(df1.app_id)]                          ####THIS IS NOT WORKING AND THE TAG_BEFORE_RELEASE DOESNT ACTUALLY GET REMOVED
                                                                    ####BUT YOU CHANGE THE CODE IN STEP4 TO REMOVE IT SO IT GETS DROPPED LATER
# convert the 'Date' column to datetime format
df2['release_date']= pd.to_datetime(df2['release_date'])
df2['tag_date']= pd.to_datetime(df2['tag_date'])

#CREATE A COLUMN TO INDICATE HOW MANY MONTHS BETWEEN RELEASE AND EACH TAG DATE

df2['nb_months'] = ((df2.tag_date - df2.release_date)/np.timedelta64(1, 'M'))
df2['nb_months'] = df2['nb_months'].astype(int)

# df2.to_csv("test2222.csv")

full_df2 = pd.DataFrame(columns=df2.columns)

ids_to_check = list(set(df2['app_id'].tolist()))

# ## ONE GAME DOESNT HAVE TAGS AT 6 MONTHS SO REMOVE IT FROM THE DF                     #### HOW DID YOU CHECK FOR THIS???????
# #875230
# I REMOVED THE GAME FROM THE CSVS FOLDER INSTEAD
# CAN USE THIS IF THERE ARE MULTIPLE GAMES THOUGH
# FOR SOME REASON ITS NOT WORKING FOR THE EARLIEST TAGS DF ABOVE
# ids_to_check.remove(875230)

counter = 0

for current_id in ids_to_check:

    counter += 1

    try:
        current_idx = df2['tag_date'].loc[(df2['app_id'] == current_id) & (df2['nb_months'] == 12)].idxmin()

        print(f"success, adding t2 tags for game {current_id}")

        temp_df = df2.loc[df2.index == current_idx,:]

        full_df2 = pd.concat([full_df2, temp_df], ignore_index=True, sort=False)
    
    except Exception as e:
        print(current_id)
        print(e)

# REORDER THE COLUMNS OF THE 6MO DF SO ALL TAG CODES ARE AT THE END
# THIS IS SO RENAMING THEM IS EASIER

cols = full_df2.columns.tolist()

# print(len(cols))
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append(cols[cnum])
# print(xxxx)

## THE COLUMN WITH # OF MONTHS BETWEEN RELEASE DATE AND TAG DATE IS DROPPED
myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,438]
myorder = myorder + list(np.arange(13,438,1)) + [439,440]
mylist = [cols[i] for i in myorder]
full_df2 = full_df2[mylist]

# cols = full_df.columns.tolist()
# print(len(cols))
# yyyy = []
# for cnum in range(len(cols)):
#     yyyy.append(cols[cnum])
# print(yyyy)

# print(full_df.columns[1:15])
# print(full_df2.columns[1:15])

# print(len(full_df.columns))
# print(len(full_df2.columns))


full_df2.to_csv("step6_tags_t2.csv", index=False)

# STEP 7 - SCRAPE API DATA

import requests
import json
import pandas as pd
import time
import datetime
import numpy as np

# query_games_df = pd.read_csv('step6_tags_t1.csv')

# all_app_ids = query_games_df['app_id'].tolist()
# # list_of_app_ids_to_check = all_app_ids


# ############################################################################
# #### ADDED THIS BECAUSE YOU ALREADY SCRAPED MOST OF THE GAMES BEFORE SO YOU DON'T NEED TO SCRAPE ALL OF THEM

# already_scraped_df = pd.read_csv("./t2_6mo_files/step7_scraped_api_data_rd1.csv")

# already_scraped_id_list = already_scraped_df.app_id.tolist()

# list_of_app_ids_to_check = []

# for id in all_app_ids:
#     if id not in already_scraped_id_list:
#         list_of_app_ids_to_check.append(id)

# ############################################################################

# # create blank dataframe and reorder columns

# all_df = pd.DataFrame(columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
#                                              'avg_pt_2weeks','initial_price','current_price','ccu',
#                                              'lang_1','lang_2','lang_3','lang_4','lang_5',
#                                              'lang_6','lang_7','lang_8','lang_9','lang_10',
#                                              'genre_1','genre_2','genre_3','genre_4','genre_5'])

# # logf = open("failed_games.txt", "w")

# fail_counter = []

# for i in range(len(list_of_app_ids_to_check)):

#     print(f"checking #{i}: {int(list_of_app_ids_to_check[i])}")
#     try:
        

#         response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={int(list_of_app_ids_to_check[i])}', timeout=10).text

#         response_info = json.loads(response)

#         app_id = response_info['appid']

#         pos_rev_num = response_info['positive']
#         neg_rev_num = response_info['negative']
#         usr_score = response_info['userscore']

#         avg_pt_forever = response_info['average_forever']
#         avg_pt_2weeks = response_info['average_2weeks']
#         initial_price = response_info['initialprice']
#         current_price = response_info['price']
#         ccu = response_info['ccu']

#         # split the string into two
#         owners_string = response_info['owners']

#         owners_vals = owners_string.split(" .. ")

#         clean_owners_vals = []

#         for string in owners_vals:
#             new_string = string.replace(",", "")
#             clean_owners_vals.append(new_string)

#         if len(clean_owners_vals) > 0:
#             owners_min = int(clean_owners_vals[0])
#             owners_max = int(clean_owners_vals[1])
#         if len(clean_owners_vals) == 0:
#             owners_min = 999999
#             owners_max = 999999 

#         genre_list = response_info['genre'].split(", ")

#         if len(genre_list) < 11:
#             number_of_nas_to_append = 10 - len(genre_list)

#             for j in range(number_of_nas_to_append):
#                 genre_list.append("NA")    
        
#         else:
#             # logf.write(f"{app_id}\n")
#             print(f"more than 10 game #{app_id}")

#         lang_list = response_info['languages'].split(", ")

#         if len(lang_list) < 11:
#             number_of_nas_to_append = 10 - len(lang_list)

#             for j in range(number_of_nas_to_append):
#                 lang_list.append("NA")  

#         row_to_add = {'app_id':[app_id],
#                     'pos_rev_num':[pos_rev_num],
#                     'neg_rev_num':[neg_rev_num],
#                     'usr_score':[usr_score],
#                     'avg_pt_forever':[avg_pt_forever],
#                     'avg_pt_2weeks':[avg_pt_2weeks],
#                     'initial_price':[initial_price],
#                     'current_price':[current_price],
#                     'ccu':[ccu],

#                     'lang_1':[lang_list[0]],
#                     'lang_2':[lang_list[1]],
#                     'lang_3':[lang_list[2]],
#                     'lang_4':[lang_list[3]],
#                     'lang_5':[lang_list[4]],
#                     'lang_6':[lang_list[5]],
#                     'lang_7':[lang_list[6]],
#                     'lang_8':[lang_list[7]],
#                     'lang_9':[lang_list[8]],
#                     'lang_10':[lang_list[9]],

#                     'genre_1':[genre_list[0]],
#                     'genre_2':[genre_list[1]],
#                     'genre_3':[genre_list[2]],
#                     'genre_4':[genre_list[3]],
#                     'genre_5':[genre_list[4]],
#                     'genre_6':[genre_list[5]],
#                     'genre_7':[genre_list[6]],
#                     'genre_8':[genre_list[7]],
#                     'genre_9':[genre_list[8]],
#                     'genre_10':[genre_list[9]]}

#         df = pd.DataFrame(row_to_add, columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
#                                                 'avg_pt_2weeks','initial_price','current_price','ccu',
#                                                 'lang_1','lang_2','lang_3','lang_4','lang_5',
#                                                 'lang_6','lang_7','lang_8','lang_9','lang_10',
#                                                 'genre_1','genre_2','genre_3','genre_4','genre_5',
#                                                 'genre_6','genre_7','genre_8','genre_9','genre_10'])   

#         all_df = pd.concat([all_df,df])

#         #print(all_df)

#         print(f"success for game #{i} of {len(list_of_app_ids_to_check)}")


#         time.sleep(2)

#     except Exception as e:
#         print(f"Game #{i} failed -- ID# {list_of_app_ids_to_check[i]} failed")

#         fail_counter.append(i)
#         #print(e)

# print("failed games list:")
# print(fail_counter)


# #########################################
# # CHECK HERE TO SEE WHICH OF THE 476 GAMES FAILED

# all_df.to_csv('step7_scraped_api_data_rd2.csv', index=False)

##################################################################
# WHEN YOU HAVE THE DATA FOR ALL GAMES THEN merge with previous file

all_df = pd.read_csv('step7_scraped_api_data.csv', index_col=False)

step3_df = pd.read_csv('step6_tags_t1.csv', index_col=False)

step_4_df = pd.merge(step3_df, all_df, on="app_id")


# REORDER COLUMNS

# for i in range(len(step_4_df.columns)):
#     print(i)
#     print(step_4_df.columns[i])

cols = step_4_df.columns.tolist()

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")

myorder = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
myorder = myorder + list(np.arange(441,469,1)) + list(np.arange(14,440,1))
mylist = [cols[i] for i in myorder]
step_4_df = step_4_df[mylist]

# cols = step_4_df.columns.tolist()
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))

step_4_df.to_csv("step7_result.csv", index=False)

# STEP 8 MERGE ti and t2 TAGS

import pandas as pd

#MERGE THE COLUMNS FROM THE TWO DATASETS WITH EARLIEST AND 6 MO TAGS
pd.set_option('display.max_rows', 100)

df1 = pd.read_csv("step7_result.csv")
df2 = pd.read_csv("step6_tags_t2.csv")

# CHANGE THE NAMES OF THE COLUMNS IN THE 6 MONTH DF STARTING AFTER WITH 14


for colnum in range(13,len(df2.columns)):       #because 0 indexed to start at 14th column use 13
    
    orig_col_name = df2.columns[colnum]
    new_col_name = f"t2_{orig_col_name}"                                                                       ###### YOU SHOULD USE REPLACE HERE INSTEAD
    df2.rename(columns = {orig_col_name : new_col_name}, inplace = True)

print(len(df1.columns))
print(len(df2.columns))

mgd_df = pd.merge(df1, df2, on="app_id")

print(len(mgd_df.columns))

mgd_df.drop(mgd_df.filter(regex='_y').columns, axis=1, inplace=True)
# mgd_df = mgd_df.loc[:,~mgd_df.columns.str.endswith('_y')]

print(len(mgd_df.columns))

## SOME TAGS ARE MISSPELT OR DONT EXIST ANYMORE SO REMOVE THEM ### YOU DON"T NEED TO DO THIS ANYMORE B/C YOU DID IT IN STEP 2
#mgd_df = mgd_df.drop('tag_999999', 1)
#mgd_df = mgd_df.drop('t6_tag_999999', 1)
#mgd_df = mgd_df.drop('tag_5144', 1)
#mgd_df = mgd_df.drop('t6_tag_5144', 1)
#mgd_df = mgd_df.drop('tag_1694', 1)
#mgd_df = mgd_df.drop('t6_tag_1694', 1)
#mgd_df = mgd_df.drop('tag_134316', 1)
#mgd_df = mgd_df.drop('t6_tag_134316', 1)

# mgd_df.drop(mgd_df.filter(regex='999999').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='5144').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='1694').columns, axis=1, inplace=True)
# mgd_df.drop(mgd_df.filter(regex='134316').columns, axis=1, inplace=True)

mgd_df.to_csv("step8_result.csv", index=False)

# STEP 10 - SUBSET DATA

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

import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

df = pd.read_csv("step10_result.csv")

# cols = df.columns.tolist()
# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))

###################################################################################################
#         # DV 1: Consensus between producer's original tags and tags after one year
#         # Test Jaccard similarity between the vector of tags at t0 and t1
#         # If there are more tags at t1 than t0 use the top tags by count
#         # Added to dataframe as column 'jac_sim'

def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))

jac_sim = []

for current_row_num in range(len(df)):

    # # GET VECTOR OF PRODUCER TAGS AT t0

    t0_df = df.iloc[:,114:538]

    t0_df.replace(np.nan,0)

    tag_cols = []
    for i in t0_df.columns:
        tag_cols.append(str(i))

    tag_counts = []
    for i in range(len(t0_df.columns)):
        tag_counts.append(int(t0_df.iloc[current_row_num,i]))

    # print(tag_cols)
    # print(tag_counts)

    pos_tags = []

    for i in range(len(tag_counts)):
        if tag_counts[i] > 0:
            pos_tags.append(tag_cols[i])

    # print(pos_tags)

    # # GET VECTOR OF TAGS AT t2
    t1_df = df.iloc[:,541:966]

    t1_df.replace(np.nan,0)

    t1_tag_cols = []
    for i in t1_df.columns:
        t1_tag_cols.append(str(i))

    t1_tag_counts = []
    for i in range(len(t1_df.columns)):
        t1_tag_counts.append(int(t1_df.iloc[current_row_num,i]))

    # print(t1_tag_cols)
    # print(t1_tag_counts)

    # SORT THE t1 TAGS BY COUNT 
    t1_pos_cols = []
    t1_pos_counts = []

    for i in range(len(t1_tag_counts)):
        if t1_tag_counts[i] > 0:
            t1_pos_cols.append(t1_tag_cols[i])
            t1_pos_counts.append(t1_tag_counts[i])

    # print(t1_pos_cols)
    # print(t1_pos_counts)

    sorted_t1_pos_cols = [x for _, x in sorted(zip(t1_pos_counts,t1_pos_cols),reverse=True)]

    sorted_t1_pos_counts = sorted(t1_pos_counts, reverse=True)

    # print(sorted_t1_pos_cols)
    # print(sorted_t1_pos_counts)

    # KEEP ONLY THE TOP N TAGS FROM t1 WHERE N IS THE NUMBER OF TAGS AT t0

    how_many_t0_tags = len(pos_tags)

    # print(pos_tags)
    shortened_sorted_t1_pos_cols = sorted_t1_pos_cols[0:how_many_t0_tags]

    renamed_shortened_sorted_t1_pos_cols = []

    for tag_name in shortened_sorted_t1_pos_cols:
        renamed_shortened_sorted_t1_pos_cols.append(tag_name.replace("t2_",""))

    # print(renamed_shortened_sorted_t1_pos_cols)

    #CAlCULATE JACCARD SIMILARITY BETWEEN t0 and t1
    try:
        jac_sim.append(jaccard_similarity(pos_tags, renamed_shortened_sorted_t1_pos_cols))
    except Exception as e:
        jac_sim.append(999999)

df['jac_sim'] = pd.Series(jac_sim)

###################################################################################################
#         # DV 1: Consensus between producer's original tags and tags after one year
#         # DO A SIMPLE COUNT OF THE NUMBER OF NEW TAGS ADDED THAT WERE ADDED IN ADDITION TO THE ONES ORIGINALLY USED BY PRODUCER

novel_tags_count = []
pos_tags = []
replaced_tags_count = []

for current_row_num in range(len(df)):

    # # GET VECTOR OF PRODUCER TAGS AT t0

    t0_df = df.iloc[:,114:538]

    t0_df.replace(np.nan,0)

    tag_cols = []
    for i in t0_df.columns:
        tag_cols.append(str(i))

    tag_counts = []
    for i in range(len(t0_df.columns)):
        tag_counts.append(int(t0_df.iloc[current_row_num,i]))
        # tag_counts.append(int(t0_df.iloc[0,i]))

    # print(tag_cols)
    # print(tag_counts)
    # print("\n")

    # GET VECTOR OF ALL TAGS AT t1
    t1_df = df.iloc[:,541:966]

    t1_df.replace(np.nan,0)

    t1_tag_cols = []
    for i in t1_df.columns:
        t1_tag_cols.append(str(i))

    t1_tag_counts = []
    for i in range(len(t1_df.columns)):
        t1_tag_counts.append(int(t1_df.iloc[current_row_num,i]))
        # t1_tag_counts.append(int(t1_df.iloc[0,i]))

    # print(t1_tag_cols)
    # print(t1_tag_counts)
    # print("\n")

    # GET VECTOR OF ONLY TAG NAMES FOR POSITIVE TAGS AT t0

    t0_pos_tags = []

    for i in range(len(tag_counts)):
        if tag_counts[i] > 0:
            t0_pos_tags.append(tag_cols[i])

    # GET VECTOR OF ONLY TAG NAMES WITH POSITIVE COUNTS AT t1

    t1_pos_tags_name = []
    t1_pos_tags_counts = []

    for i in range(len(t1_tag_counts)):
        if t1_tag_counts[i] > 0:
            t1_pos_tags_name.append(t1_tag_cols[i])
            t1_pos_tags_counts.append(t1_tag_counts[i])

    # print(t1_pos_tags_name)
    # print(t1_pos_tags_counts)

    # SORT VECTOR OF TAG NAMES BASED ON COUNTS

    t1_tag_cols_sorted = [x for _, x in sorted(zip(t1_pos_tags_counts, t1_pos_tags_name), reverse=True, key=lambda pair: pair[0])]

    # print(t1_tag_cols_sorted)

    # KEEP ONLY THE TOP N t1 TAGS WHERE N IS THE NUMBER OF t0 TAGS

    # print(f"time 0: {t0_pos_tags}")
    # print(f"time 0 length: {len(t0_pos_tags)}")

    # print(f"time 1: {t1_tag_cols_sorted}")
    # print(f"time 1 length: {len(t1_tag_cols_sorted)}")

    t1_tag_cols_sorted = t1_tag_cols_sorted[0:len(t0_pos_tags)]

    # print(f"time 1: {t1_tag_cols_sorted}")
    # print(f"time 1 length: {len(t1_tag_cols_sorted)}")

    # REMOVE THE t2_ PREFIX FROM THE VECTOR OF t1 COLUMNS SO THEY CAN BE COMPARED

    renamed_t1_tag_cols_sorted = []
    for tag_name in t1_tag_cols_sorted:
        renamed_t1_tag_cols_sorted.append(tag_name.replace("t2_",""))

    # GET NUMBER OF TAGS THAT WERE SWITCHED

    intersection = [value for value in renamed_t1_tag_cols_sorted if value not in t0_pos_tags]

    # print("\n")
    # print(intersection)
    # print(len(intersection))

    # if intersection is None:
    #     replaced_tags_count.append(0)
    # else:
    replaced_tags_count.append(int(len(intersection)))


df['replaced_tags_count'] = replaced_tags_count


###################################################################################################
#         # DV 1: Jaccard similarity between vector of producer's original tags and same length vector of tags after one year sorted by count
#         # DO A SIMPLE COMPARISON OF THE NUMBER OF NEW TAGS ADDED THAT WERENT ORIGINALLY USED BY PRODUCER


pos_tags = []
jac_sim_equal_length = []

for current_row_num in range(len(df)):

    # # GET VECTOR OF PRODUCER TAGS AT t0

    t0_df = df.iloc[:,114:538]

    t0_df.replace(np.nan,0)

    tag_cols = []
    for i in t0_df.columns:
        tag_cols.append(str(i))

    tag_counts = []
    for i in range(len(t0_df.columns)):
        tag_counts.append(int(t0_df.iloc[current_row_num,i]))
        # tag_counts.append(int(t0_df.iloc[0,i]))

    # print(tag_cols)
    # print(tag_counts)
    # print("\n")

    # GET VECTOR OF ALL TAGS AT t1
    t1_df = df.iloc[:,541:966]

    t1_df.replace(np.nan,0)

    t1_tag_cols = []
    for i in t1_df.columns:
        t1_tag_cols.append(str(i))

    t1_tag_counts = []
    for i in range(len(t1_df.columns)):
        t1_tag_counts.append(int(t1_df.iloc[current_row_num,i]))
        # t1_tag_counts.append(int(t1_df.iloc[0,i]))

    # print(t1_tag_cols)
    # print(t1_tag_counts)
    # print("\n")

    # GET VECTOR OF ONLY TAG NAMES FOR POSITIVE TAGS AT t0

    t0_pos_tags = []

    for i in range(len(tag_counts)):
        if tag_counts[i] > 0:
            t0_pos_tags.append(tag_cols[i])

    # GET VECTOR OF ONLY TAG NAMES WITH POSITIVE COUNTS AT t1

    t1_pos_tags_name = []
    t1_pos_tags_counts = []

    for i in range(len(t1_tag_counts)):
        if t1_tag_counts[i] > 0:
            t1_pos_tags_name.append(t1_tag_cols[i])
            t1_pos_tags_counts.append(t1_tag_counts[i])

    # print(t1_pos_tags_name)
    # print(t1_pos_tags_counts)

    # SORT VECTOR OF TAG NAMES BASED ON COUNTS

    t1_tag_cols_sorted = [x for _, x in sorted(zip(t1_pos_tags_counts, t1_pos_tags_name), reverse=True, key=lambda pair: pair[0])]

    # print(t1_tag_cols_sorted)

    # KEEP ONLY THE TOP N t1 TAGS WHERE N IS THE NUMBER OF t0 TAGS

    # print(f"time 0: {t0_pos_tags}")
    # print(f"time 0 length: {len(t0_pos_tags)}")

    # print(f"time 1: {t1_tag_cols_sorted}")
    # print(f"time 1 length: {len(t1_tag_cols_sorted)}")

    t1_tag_cols_sorted = t1_tag_cols_sorted[0:len(t0_pos_tags)]

    # print(f"time 1: {t1_tag_cols_sorted}")
    # print(f"time 1 length: {len(t1_tag_cols_sorted)}")

    # REMOVE THE t2_ PREFIX FROM THE VECTOR OF t1 COLUMNS SO THEY CAN BE COMPARED

    renamed_t1_tag_cols_sorted = []
    for tag_name in t1_tag_cols_sorted:
        renamed_t1_tag_cols_sorted.append(tag_name.replace("t2_",""))

    # GET NUMBER OF TAGS THAT WERE SWITCHED

    # intersection = [value for value in renamed_t1_tag_cols_sorted if value in t0_pos_tags]

    # print("\n")
    # print(intersection)
    # print(len(intersection))

    # if intersection is None:
    #     replaced_tags_count.append(0)
    # else:
    try:
        jac_sim_equal_length.append(jaccard_similarity(renamed_t1_tag_cols_sorted[1:len(t0_pos_tags)], t0_pos_tags))
    except Exception as e:
        jac_sim_equal_length.append(999999)

df['jac_sim_equal_length'] = jac_sim_equal_length











###################################################################################################
#         # DV 1: Consensus between producer's original tags and tags after one year
#         # DO A SIMPLE COMPARISON OF THE NUMBER OF NEW TAGS ADDED THAT WERENT ORIGINALLY USED BY PRODUCER


novel_tags_count = []

for current_row_num in range(len(df)):

    # # GET VECTOR OF PRODUCER TAGS AT t0

    t0_df = df.iloc[:,114:538]

    t0_df.replace(np.nan,0)

    tag_cols = []
    for i in t0_df.columns:
        tag_cols.append(str(i))

    tag_counts = []
    for i in range(len(t0_df.columns)):
        tag_counts.append(int(t0_df.iloc[current_row_num,i]))
        # tag_counts.append(int(t0_df.iloc[0,i]))

    # print(tag_cols)
    # print(tag_counts)

    t0_pos_tags = []

    for i in range(len(tag_counts)):
        if tag_counts[i] > 0:
            t0_pos_tags.append(tag_cols[i])

    # print(pos_tags)

    # # GET VECTOR OF TAGS AT t2
    t1_df = df.iloc[:,541:966]

    t1_df.replace(np.nan,0)

    t1_tag_cols = []
    for i in t1_df.columns:
        t1_tag_cols.append(str(i))

    t1_tag_counts = []
    for i in range(len(t1_df.columns)):
        t1_tag_counts.append(int(t1_df.iloc[current_row_num,i]))
        # t1_tag_counts.append(int(t1_df.iloc[0,i]))

    # print(t1_tag_cols)
    # print(t1_tag_counts)

    # SORT THE t1 TAGS BY COUNT 
    t1_pos_cols = []

    for i in range(len(t1_tag_counts)):
        if t1_tag_counts[i] > 0:
            t1_pos_cols.append(t1_tag_cols[i])

    renamed_t1_pos_cols = []
    for tag_name in t1_pos_cols:
        renamed_t1_pos_cols.append(tag_name.replace("t2_",""))

    # print(t0_pos_tags)
    # print(renamed_t1_pos_cols)

    intersection = [value for value in renamed_t1_pos_cols if value not in t0_pos_tags]

    novel_tags_count.append(int(len(intersection)))

df['novel_tags_count'] = novel_tags_count


###################################################################################################
# DV 2: entropy of t2 tags

# GET VECTOR OF TAGS AT t2 AND CALCULATE ENTROPY FOR EACH ROW
entropies = []
for current_row_num in range(len(df)):

    t1_df = df.iloc[current_row_num,541:966]
    t1_df.replace(np.nan,0)

    t1_tag_counts = t1_df.values
    t1_tag_cols = t1_df.index

    t1_tag_counts_clean = []
    t1_tag_cols_clean = []
    for i in range(len(t1_tag_counts)):
        if t1_tag_counts[i] > 0:
            t1_tag_counts_clean.append(int(t1_tag_counts[i]))
            t1_tag_cols_clean.append(t1_tag_cols[i])

    # print(t1_tag_counts_clean)
    # print(t1_tag_cols_clean)

    sum_total = sum(t1_tag_counts_clean)

    data = [x / sum_total for x in t1_tag_counts_clean]

    # print(data)

    # fig = plt.figure()                                                               
    # ax = fig.gca()  #get current axes
    # width = 1
    # ax.bar(t1_tag_cols_clean, t1_tag_counts_clean, width, align='center')
    # plt.xticks(rotation = 45) # Rotates X-Axis Ticks by 45-degrees
    # plt.savefig("./figures/barplot222222.png")

    entropies.append(scipy.stats.entropy(data, base=2))

df['t2_entropy'] = pd.Series(entropies)

###################################################################################################
# IV: SIMPLE MEASURE OF GENRE SPANNING (COUNT # OF GENRES)

genres_df = df.iloc[:,33:43]

genres_df = genres_df.replace(np.nan,0)

# print(genres_df)

num_of_genres_list = (genres_df == 0).astype(int).sum(axis=1).values

num_of_genres_list = [10 - x for x in num_of_genres_list]

# print(num_of_genres_list)

df['genre_count'] = num_of_genres_list

###################################################################################################


df.to_csv("step12_result.csv", index=False)
