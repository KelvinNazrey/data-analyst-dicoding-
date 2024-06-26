import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import zipfile
import requests
import io
import matplotlib.image as mpimg
import urllib.request

# Function to download and extract ZIP file
def download_and_extract_zip(url, extract_to='.'):
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(extract_to)

# URL to the raw ZIP file content
zip_url = "https://github.com/KelvinNazrey/data-analyst-dicoding-/raw/main/all_data.zip"
download_and_extract_zip(zip_url)

# Load data from the extracted CSV file
all_data = pd.read_csv("all_data.csv")

# Function to plot Brazil map
def plot_brazil_map(data):
    # Load the Brazil map image
    brazil = mpimg.imread(urllib.request.urlopen('https://i.pinimg.com/originals/3a/0c/e1/3a0ce18b3c842748c255bc0aa445ad41.jpg'), 'jpg')
    fig, ax = plt.subplots(figsize=(10, 10))
    data.plot(kind="scatter", x="geolocation_lng", y="geolocation_lat", alpha=0.5, s=0.5, c='darkred', ax=ax)
    ax.imshow(brazil, extent=[-73.98283055, -33.8, -33.75116944, 5.4], zorder=0)
    ax.axis('off')
    plt.title('Geolocations in Brazil', fontsize=18, weight='bold')
    st.pyplot(fig)

# Set option to avoid PyplotGlobalUseWarning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Question 1: Top Selling and Lowest Selling Products
st.header("Question 1: Top Selling and Lowest Selling Products")
sum_order_items_df = all_data.groupby("product_category_name_english")["product_id"].count().reset_index()
sum_order_items_df = sum_order_items_df.rename(columns={"product_id": "products"})
sum_order_items_df = sum_order_items_df.sort_values(by="products", ascending=False).head(10)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors1 = ["#4CAF50", "#A5D6A7", "#C8E6C9", "#E8F5E9", "#F1F8E9"]
colors2 = ["#FF7043", "#FFAB91", "#FFCCBC", "#FFE0B2", "#FFF3E0"]

# Top Selling Products
sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.head(5), palette=colors1, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Products", fontsize=15)
ax[0].set_title("Top Selling Products", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].grid(True, which='major', axis='x', linestyle='--')

# Lowest Selling Products
sns.barplot(x="products", y="product_category_name_english", data=sum_order_items_df.sort_values(by="products", ascending=True).head(5), palette=colors2, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Products", fontsize=15)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Lowest Selling Products", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].grid(True, which='major', axis='x', linestyle='--')

plt.suptitle("Top Selling and Lowest Selling Products", fontsize=20)
plt.tight_layout(rect=[0, 0, 1, 0.95])
st.pyplot(plt.gcf())

# Question 2: Customer Satisfaction in 2018
st.header("Question 2: Customer Satisfaction in 2018")
all_data['review_creation_date'] = pd.to_datetime(all_data['review_creation_date'], errors='coerce')
all_data = all_data.dropna(subset=['review_creation_date'])  # Drop rows with invalid dates
last_six_months_data = all_data[all_data['review_creation_date'] >= all_data['review_creation_date'].max() - pd.DateOffset(months=7)]

plt.figure(figsize=(10, 5))
sns.countplot(x=last_six_months_data['review_creation_date'].dt.month,
              hue=last_six_months_data['review_score'],
              palette="viridis")

plt.title("Customer Satisfaction in 2018", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Count of Reviews")
plt.legend(title="Review Score", loc='upper right', bbox_to_anchor=(1.2, 1))

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug']
plt.xticks(range(0, 8), months)
st.pyplot(plt.gcf())

# Question 3: Customer Satisfaction Rating
st.header("Question 3: Customer Satisfaction Rating")
review_scores = all_data['review_score'].value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
sns.barplot(x=review_scores.index,
            y=review_scores.values,
            order=review_scores.index,
            palette="viridis")

plt.title("Rating by customers for service", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Count")
plt.xticks(fontsize=12)
st.pyplot(plt.gcf())

