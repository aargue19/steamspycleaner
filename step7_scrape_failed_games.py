import requests
import json
import pandas as pd
import time
import datetime
import numpy as np

# query_games_df = pd.read_csv('step6_tags_t1.csv')

# all_app_ids = query_games_df['app_id'].tolist()

# list_of_app_ids_to_check = all_app_ids

# # create blank dataframe and reorder columns

# all_df = pd.DataFrame(columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
#                                              'avg_pt_2weeks','initial_price','current_price','ccu',
#                                              'lang_1','lang_2','lang_3','lang_4','lang_5',
#                                              'lang_6','lang_7','lang_8','lang_9','lang_10',
#                                              'genre_1','genre_2','genre_3','genre_4','genre_5'])

# # logf = open("failed_games.txt", "w")

# fail_counter = []

# # list_of_failed_games = [9, 10, 12, 18, 19, 33, 39, 57, 113, 120, 130, 163, 180, 184, 199, 224, 232, 255, 288, 302, 328, 333, 355, 360, 364, 366, 367, 372, 374, 
# # 377, 380, 386, 390, 394, 396, 400, 407, 408, 416, 417, 418, 422, 427, 429, 430, 442, 445, 457, 460, 491, 516, 539, 589, 595, 621, 634, 697, 700, 707, 709, 719, 
# # 720, 722, 767, 769, 808, 810, 821, 845, 849, 850, 856, 858, 863, 868, 871, 873, 912, 947, 951, 965, 981, 1006, 1017, 1034, 1041, 1045, 1059, 1065, 1093, 1094, 
# # 1107, 1109, 1140, 1163, 1171, 1180, 1203, 1220, 1224, 1230, 1255, 1264, 1266, 1283, 1294, 1306, 1381, 1385, 1414, 1433, 1444, 1486, 1533, 1600, 1601, 1603]


# list_of_failed_games = [328, 355, 367, 429, 700, 965, 1017, 1171, 1264, 1306]

# for i in range(len(list_of_app_ids_to_check)):

#     if (i in list_of_failed_games):

#         print(f"checking #{i}: {int(list_of_app_ids_to_check[i])}")
#         try:
            

#             response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={int(list_of_app_ids_to_check[i])}', timeout=10).text

#             response_info = json.loads(response)

#             app_id = response_info['appid']

#             pos_rev_num = response_info['positive']
#             neg_rev_num = response_info['negative']
#             usr_score = response_info['userscore']

#             avg_pt_forever = response_info['average_forever']
#             avg_pt_2weeks = response_info['average_2weeks']
#             initial_price = response_info['initialprice']
#             current_price = response_info['price']
#             ccu = response_info['ccu']

#             # split the string into two
#             owners_string = response_info['owners']

#             owners_vals = owners_string.split(" .. ")

#             clean_owners_vals = []

#             for string in owners_vals:
#                 new_string = string.replace(",", "")
#                 clean_owners_vals.append(new_string)

#             if len(clean_owners_vals) > 0:
#                 owners_min = int(clean_owners_vals[0])
#                 owners_max = int(clean_owners_vals[1])
#             if len(clean_owners_vals) == 0:
#                 owners_min = 999999
#                 owners_max = 999999 

#             genre_list = response_info['genre'].split(", ")

#             if len(genre_list) < 11:
#                 number_of_nas_to_append = 10 - len(genre_list)

#                 for j in range(number_of_nas_to_append):
#                     genre_list.append("NA")    
            
#             else:
#                 # logf.write(f"{app_id}\n")
#                 print(f"more than 10 game #{app_id}")

#             lang_list = response_info['languages'].split(", ")

#             if len(lang_list) < 11:
#                 number_of_nas_to_append = 10 - len(lang_list)

#                 for j in range(number_of_nas_to_append):
#                     lang_list.append("NA")  

#             row_to_add = {'app_id':[app_id],
#                         'pos_rev_num':[pos_rev_num],
#                         'neg_rev_num':[neg_rev_num],
#                         'usr_score':[usr_score],
#                         'avg_pt_forever':[avg_pt_forever],
#                         'avg_pt_2weeks':[avg_pt_2weeks],
#                         'initial_price':[initial_price],
#                         'current_price':[current_price],
#                         'ccu':[ccu],

#                         'lang_1':[lang_list[0]],
#                         'lang_2':[lang_list[1]],
#                         'lang_3':[lang_list[2]],
#                         'lang_4':[lang_list[3]],
#                         'lang_5':[lang_list[4]],
#                         'lang_6':[lang_list[5]],
#                         'lang_7':[lang_list[6]],
#                         'lang_8':[lang_list[7]],
#                         'lang_9':[lang_list[8]],
#                         'lang_10':[lang_list[9]],

#                         'genre_1':[genre_list[0]],
#                         'genre_2':[genre_list[1]],
#                         'genre_3':[genre_list[2]],
#                         'genre_4':[genre_list[3]],
#                         'genre_5':[genre_list[4]],
#                         'genre_6':[genre_list[5]],
#                         'genre_7':[genre_list[6]],
#                         'genre_8':[genre_list[7]],
#                         'genre_9':[genre_list[8]],
#                         'genre_10':[genre_list[9]]}

#             df = pd.DataFrame(row_to_add, columns = ['app_id','pos_rev_num','neg_rev_num','usr_score','avg_pt_forever',
#                                                     'avg_pt_2weeks','initial_price','current_price','ccu',
#                                                     'lang_1','lang_2','lang_3','lang_4','lang_5',
#                                                     'lang_6','lang_7','lang_8','lang_9','lang_10',
#                                                     'genre_1','genre_2','genre_3','genre_4','genre_5',
#                                                     'genre_6','genre_7','genre_8','genre_9','genre_10'])   

#             all_df = pd.concat([all_df,df])

#             #print(all_df)

#             print(f"success for game #{i} of {len(list_of_app_ids_to_check)}")


#             time.sleep(2)

#         except Exception as e:
#             print(f"Game #{i} failed -- ID# {list_of_app_ids_to_check[i]} failed")

#             fail_counter.append(i)
#             print(e)

#     print("failed games list:")
#     print(fail_counter)


# #########################################
# # CHECK HERE TO SEE WHICH OF THE 476 GAMES FAILED

# all_df.to_csv('step7_scraped_api_data_failed_games2.csv', index=False)
# all_df.to_csv('step7_scraped_api_data_failed_games2.csv', index=False)


# all_df = pd.read_csv('step7_scraped_api_data_failed_games.csv', index_col=False)
all_df = pd.read_csv('step7_scraped_api_data_failed_games2.csv', index_col=False)

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


step_4_df.to_csv("step7_result_failed_games2.csv", index=False)