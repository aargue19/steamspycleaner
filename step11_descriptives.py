import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("step10_result.csv", low_memory=False)



# # DISTRIBUTION OF PRICES
# prices = df['price_x']
# plt.figure(0)
# plt.hist(prices, bins=100)
# plt.xlabel("price in cents")
# plt.ylabel("count")
# plt.savefig('./figures/prices_hist.png') 

# # DISTRIBUTION OF RELEASE DATES
# df['release_date_x'] = pd.to_datetime(df['release_date_x'])
# plt.figure(1)
# plt.hist(df["release_date_x"], bins=100)
# plt.xlabel("release date")
# plt.ylabel("count")
# plt.savefig('./figures/release_dates_hist.png') 

# # DISTRIBUTION OF GENRES IN GENRE 1 COLUMN
# genres = df['genre_1'].value_counts()
# plt.figure(2)
# plt.bar(genres.index, genres.values)
# plt.xlabel("genre")
# plt.xticks(rotation=45)
# plt.ylabel("count")
# plt.savefig('./figures/genres_bar.png') 

# DISTRIBUTION OF POSITIVITY OF REVIEWS
# df['positivity'] = df['pos_rev_num'].astype(np.int64) /  (df['pos_rev_num'].astype(np.int64) + df['neg_rev_num'].astype(np.int64))
# plt.figure(3)
# plt.hist(df['positivity'], bins=100)
# plt.xlabel("positivity of reviews")
# plt.ylabel("count")
# plt.savefig('./figures/positivity_hist.png') 

# DISTRIBUTION OF NUMBER OF OWNERS

# print(f"games with under 100000 owners represents {round(100 * len(df['owners_x'].loc[df.owners_x < 100000]) / len(df.owners_x),2)}% of games")
# plt.figure(4)
# plt.hist(df['owners_x'].loc[df.owners_x < 100000], bins=100)
# plt.xlabel("number of owners")
# plt.ticklabel_format(style='plain')
# plt.xticks(rotation=45)
# plt.ylabel("count")
# plt.savefig('./figures/owners_under_100k_hist.png') 

plt.figure(5)
data = df['owners_x']
plt.hist(data, bins=100)
# plt.hist(df['owners_x'], bins=100, range=(100000, 7000000))
plt.xlabel("number of owners")
plt.ticklabel_format(style='plain')
plt.xticks(rotation=45)
plt.xlim(xmin=100000, xmax = 700000)
# plt.xlim(100000, 7000000)
plt.ylabel("count")
plt.tight_layout()
plt.savefig('./figures/owners_100k_and_above_hist.png') 