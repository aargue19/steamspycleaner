import pandas as pd
import numpy as np

df1 = pd.read_csv("step8_result.csv", low_memory=False)

# x1 = []
# for i in df1.columns:
#     x1.append(i)
# print(x1)
# print("\n")

# print(len(df1.columns))

df2 = pd.read_csv("step3_steamspy_scraped_data.csv")

# print(len(df2.columns))

# x1 = []
# for i in df2.columns:
#     x1.append(i)
# print("\n")

df2.rename(columns={'app_id_scrap': 'app_id'}, inplace=True)


# x1 = []
# for i in df2.columns:
#     x1.append(i)
# print(x1)
# print("\n")

mgd_df = pd.merge(df1, df2, on="app_id")

cols = mgd_df.columns.tolist()

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")


myorder = list(np.arange(0,42,1)) + list(np.arange(896,967,1)) + list(np.arange(42,896,1))  #### THE TAG_DATE COLUMN IS OUT OF PLACE BUT NOT A BIG DEAL
mylist = [cols[i] for i in myorder]
mgd_df = mgd_df[mylist]

# cols = mgd_df.columns.tolist()

# xxxx = []
# for cnum in range(len(cols)):
#     xxxx.append([cnum,cols[cnum]])
# print(xxxx)
# print(len(cols))
# print("\n")

mgd_df.to_csv("step9_result.csv", index=False)