import pandas as pd
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

df = pd.read_csv("step10_result.csv")

current_row_num = 0
pos_tags = []

novel_tags_count = []
pos_tags = []

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



        


df['replaced_tags_count'] = replaced_tags_count