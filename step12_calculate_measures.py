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