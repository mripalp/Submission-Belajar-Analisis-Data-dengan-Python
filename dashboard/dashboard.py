import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set tema seaborn
sns.set_theme(style="whitegrid")

# Menyiapkan data day_df
day_df = pd.read_csv("dashboard/main_data.csv")
day_df.drop(columns=["windspeed"], inplace=True)

# Rename kolom dan mapping nilai
day_df.rename(columns={
    "dteday": "dateday",
    "yr": "year",
    "mnth": "month",
    "weathersit": "weather_cond",
    "cnt": "count"
}, inplace=True)

day_df["month"] = day_df["month"].map({
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
})
day_df["season"] = day_df["season"].map({
    1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"
})
day_df["weekday"] = day_df["weekday"].map({
    0: "Minggu", 1: "Senin", 2: "Selasa", 3: "Rabu", 4: "Kamis", 5: "Jumat", 6: "Sabtu"
    
    # 0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"
})
day_df["weather_cond"] = day_df["weather_cond"].map({
    1: "Clear/Partly Cloudy",
    2: "Misty/Cloudy",
    3: "Light Snow/Rain",
    4: "Severe Weather"
})

# Fungsi untuk membuat DataFrame agregasi
def create_aggregated_df(df, group_col, agg_col):
    return df.groupby(by=group_col).agg({agg_col: "mean"}).reset_index()

# Filter data sesuai rentang waktu
min_date = pd.to_datetime(day_df["dateday"]).dt.date.min()
max_date = pd.to_datetime(day_df["dateday"]).dt.date.max()

with st.sidebar:
    st.image("data:image/png;base64,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") 
    st.sidebar.title("BikeTrend Insights")  
    start_date, end_date = st.date_input(
        "Rentang Waktu", min_value=min_date, max_value=max_date, value=[min_date, max_date]
    )

main_df = day_df[
    (day_df["dateday"] >= str(start_date)) & (day_df["dateday"] <= str(end_date))
]

# Dashboard
st.title("Bike Sharing Dashboard")

# Penyewaan Harian
st.subheader("Daily Trend")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Casual User", main_df["casual"].sum())
with col2:
    st.metric("Registered User", main_df["registered"].sum())
with col3:
    st.metric("Total Rentals", main_df["count"].sum())

# Grafik Berdasarkan Hari Kerja (Workingday)
st.subheader("Working Days")
workingday_rent_df = create_aggregated_df(main_df, "workingday", "count")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="workingday", y="count", data=workingday_rent_df,
    hue="workingday", palette="Blues_d", ax=ax
)

for index, row in workingday_rent_df.iterrows():
    ax.text(index, row["count"] + 10, f"{round(row['count'])}", ha="center", va="bottom", fontsize=12)

ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Hari Kerja", fontsize=16, weight="bold")
ax.set_xlabel("Hari Kerja", fontsize=14)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Bukan Hari Kerja', 'Hari Kerja'], fontsize=12)
st.pyplot(fig)

# Grafik Berdasarkan Libur (Holiday)
st.subheader("Holidays")
holiday_rent_df = create_aggregated_df(main_df, "holiday", "count")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="holiday", y="count", data=holiday_rent_df,
    hue="holiday", palette="Greens_d", ax=ax
)

for index, row in holiday_rent_df.iterrows():
    ax.text(index, row["count"] + 10, f"{round(row['count'])}", ha="center", va="bottom", fontsize=12)

ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Hari Libur", fontsize=16, weight="bold")
ax.set_xlabel("Hari Libur", fontsize=14)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
ax.set_xticks([0, 1])
ax.set_xticklabels(['Bukan Hari Libur', 'Hari Libur'], fontsize=12)
st.pyplot(fig)

# Penyewaan Berdasarkan Hari
st.subheader("Daily")
weekday_rent_df = create_aggregated_df(main_df, "weekday", "count")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x="weekday", y="count", data=weekday_rent_df,
    hue="weekday", palette="coolwarm", ax=ax
)

for index, row in weekday_rent_df.iterrows():
    ax.text(index, row["count"] + 10, f"{round(row['count'])}", ha="center", va="bottom", fontsize=12)

ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Hari dalam Seminggu", fontsize=16, weight="bold")
ax.set_xlabel("Hari dalam seminggu", fontsize=14)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
ax.set_xticks(range(7))
ax.set_xticklabels(['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])
ax.tick_params(axis="x", labelsize=12)
ax.tick_params(axis="y", labelsize=12)
st.pyplot(fig)

# Penyewaan Bulanan
st.subheader("Monthly & Year Trend")
main_df['month'] = pd.Categorical(
    main_df['month'], 
    categories=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], 
    ordered=True
)
monthly_counts = main_df.groupby(by=["month", "year"], observed=False).agg({
    "count": "sum"
}).reset_index()
fig, ax = plt.subplots(figsize=(14, 8))
sns.lineplot(
    data=monthly_counts,
    x="month",
    y="count",
    hue="year",
    palette="rocket",
    marker="o",
    ax=ax
)
ax.set_title("Jumlah Total Sepeda yang Disewakan Berdasarkan Bulan dan Tahun", fontsize=16, weight="bold")
ax.set_xlabel(None)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
ax.legend(title="Tahun", loc="upper right", fontsize=12, title_fontsize=14)
plt.tight_layout()
st.pyplot(fig)

# Penyewaan Berdasarkan Kondisi Cuaca
st.subheader("Weather-based Trend")
weather_rent_dft = main_df.groupby('weather_cond').agg({
    'count': 'mean'
}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weather_cond',
    y='count',
    hue='weather_cond',
    data=weather_rent_dft,
    palette="coolwarm",
    ax=ax
)
for index, row in weather_rent_dft.iterrows():
    ax.text(index, row["count"], f"{round(row['count'])}", ha="center", va="bottom", fontsize=12)
ax.set_title("Jumlah Pengguna Sepeda Berdasarkan Kondisi Cuaca", fontsize=16, weight="bold")
ax.set_xlabel("Kondisi Cuaca", fontsize=14)
ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
plt.tight_layout()
st.pyplot(fig)

# Penyewaan Berdasarkan Musim
# st.subheader("Seasonal Rentals Trend")
# season_rent_df = create_aggregated_df(main_df, "season", "count")
# fig, ax = plt.subplots(figsize=(12, 6))
# sns.barplot(
#     x="season", y="count", data=season_rent_df,
#     hue="season", palette="coolwarm", ax=ax
# )
# for index, row in season_rent_df.iterrows():
#     ax.text(index, row["count"], f"{round(row['count'])}", ha="center", va="bottom")
# ax.set_title("Jumlah Penyewaan Berdasarkan Musim", fontsize=16, weight="bold")
# ax.set_xlabel("Musim", fontsize=14)
# ax.set_ylabel("Jumlah Pengguna Sepeda", fontsize=14)
# ax.tick_params(axis="x", labelsize=12)
# ax.tick_params(axis="y", labelsize=12)
# st.pyplot(fig)