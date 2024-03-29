# Streamlit app
Link: [https://andao711-recommendation-system-final-file-gui-8ugoi9.streamlit.app/](https://recommendationsystem-lt0q7s5hkqt.streamlit.app/)

# Capstone Project: Tiki Recommendation System
![](img/tiki1.jpg)

A recommendation system is a type of algorithm designed to recommend or suggest things to the user based on many different factors. The recommendation system deals with a large amount of data and filters it out based on user’s preferences and interests.
### Our Task: Build a Recommendation System to help Tiki recommends and suggests products for users/customers.
### Collaborative Filtering
- Collaborative filtering relies on the preferences of similar users to offer recommendations to a particular user.
- Collaborative does not need the features of the items to be given. Every user and item is described by a feature vector or embedding.
- It creates embedding for both users and items on its own. It embeds both users and items in the same embedding space.
- It considers other users’ reactions while recommending a particular user. It notes which items a particular user likes and also the items that the users with behavior and likings like him/her likes, to recommend items to that user.
- It collects user feedbacks on different items and uses them for recommendations.

![](https://i0.wp.com/analyticsarora.com/wp-content/uploads/2022/03/collaborative-filtering-shown-visually.png?resize=800%2C600&ssl=1)
### Content-Based Filtering
- Content-Based recommender system tries to guess the features or behavior of a user given the item’s features, they react positively to.
- It makes recommendations by using keywords and attributes assigned to objects in a database and matching them to a user profile.
- The user profile is created based on data derived from a user’s actions, such as purchases, ratings (likes and dislikes), downloads, items searched for on a website and/or placed in a cart, and clicks on product links.
![](https://www.iteratorshq.com/wp-content/uploads/2021/06/content_based_collaborative_filtering.jpg)

In this project, I use Cosine with CountVectorize for Content-based filtering & ALS Pyspark model for Collaborative filtering (RMSE=1.1). 

I convert result files in ".parquet" type. It help takes less space and queries faster more than ".csv".

### Dataset:
- Link: https://drive.google.com/drive/folders/1a-np1uBVSkxeRXDbxp-dtvpLYXcTVCci?usp=sharing
- The dataset have 2 files: ProductRaw.csv, ReviewRaw.csv. The dataset contains information about products, reviews, rating for items in Mobile_Tablet, TV_Audio, Laptop, Camera, Accessory groups. It's collected on tiki.vn.
### Tech Stack:
- Language: Python
- Libraries: pandas, numpy, seaborn, matplotlib, scikit-learn, pyspark, streamlit

