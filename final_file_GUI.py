import streamlit as st
import pandas as pd
from st_aggrid import AgGrid,GridUpdateMode,DataReturnMode,ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_image_select import image_select
import warnings
warnings.filterwarnings('ignore')

#load csv
@st.cache_data(max_entries=1000)
def load_csv(file):
    df = pd.read_csv(file,index_col=0)
    return df

#load parquet
@st.cache_data(max_entries=1000)
def load_data():
    df = pd.read_parquet('ALS_top10.parquet',engine='pyarrow')
    return df

#ALS recommend
@st.cache_data(max_entries=1000)
def als_recommend(lines):
    st.write('Top Recommended Products:')
    cols = st.columns(2)
    with cols[0]:
        for i, row in lines.head().iterrows():
        # Display the recommended product
            st.write(row['item_name'])
            st.image(row['image'], width=None)
            st.write(f"<b>Rating:</b> {row['predict_rating']:.2f}", unsafe_allow_html=True)
                        
    with cols[1]:
        for i, row in lines.tail().iterrows():
        # Display the recommended product
            st.write(row['item_name'])
            st.image(row['image'], width=None)
            st.write(f"<b>Rating:</b> {row['predict_rating']:.2f}", unsafe_allow_html=True)

# Content based recommend
@st.cache_data(max_entries=1000)
def item(product_name):
  return product_images.loc[product_images['product_name']==product_name]['product_id']

@st.cache_data(max_entries=1000)
def content_based_product(item_id):
    recs=CB_top10.loc[CB_top10['product_id']==item_id]
    recs=recs.drop(['product_id','score'], axis = 1)
    recs.columns=['product_id']
    #Add product_name, image based on product_id
    s1 = product_images.set_index('product_id')['image']
    s2 = product_images.set_index('product_id')['product_name']
    recs['product_name'] = recs['product_id'].replace(s2)
    recs['image'] = recs['product_id'].replace(s1)

    # Return the dataframe
    return recs[['product_id', 'product_name', 'image']]

#img click
def img_cb(recommendations):
    img = image_select(label="Choose image",
                    images=recommendations['image'].tolist(),
                    use_container_width=False,
                    captions=recommendations['product_name'].tolist())
    return img

# Load data
df = load_data()
product_images = load_csv('Files/Product_image.csv')
customer_id_lst=load_csv('Files/customer_id.csv')
CB_top10 = load_csv("Files/CB_top10.csv")


#-----------------------------


# Set up the Streamlit app
st.markdown("<h1 style='text-align: center; color: grey;'>Data Science Capstone Project</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: blue;'>Tiki Recommendation System</h1>", unsafe_allow_html=True)

sidebar_option = st.sidebar.radio("Table of Contents", ["Business Understanding", "Collaborative Filtering", "Content-based Filtering"])

if sidebar_option == "Business Understanding":
    st.header("Business Understanding")
    st.image('img/tiki1.jpg')
    # Add some text about recommendation systems
    st.write("Build a Recommendation System to help Tiki recommends and suggests products for users/customers.")
    st.write("<h1 style='font-size: 20px;'>Collaborative Filtering</h1>", unsafe_allow_html=True)
    st.write("Collaborative filtering relies on the preferences of similar users to offer recommendations to a particular user.")
    st.write("Collaborative does not need the features of the items to be given. Every user and item is described by a feature vector or embedding.")
    st.write("It creates embedding for both users and items on its own. It embeds both users and items in the same embedding space.")
    st.write("It considers other users’ reactions while recommending a particular user. It notes which items a particular user likes and also the items that the users with behavior and likings like him/her likes, to recommend items to that user.")
    st.write("It collects user feedbacks on different items and uses them for recommendations.")
    st.image("https://i0.wp.com/analyticsarora.com/wp-content/uploads/2022/03/collaborative-filtering-shown-visually.png?resize=800%2C600&ssl=1")
    st.write("<h1 style='font-size: 20px;'>Content-Based Filtering</h1>", unsafe_allow_html=True)
    st.write("Content-Based recommender system tries to guess the features or behavior of a user given the item’s features, they react positively to.")
    st.write("It makes recommendations by using keywords and attributes assigned to objects in a database and matching them to a user profile.")
    st.write("The user profile is created based on data derived from a user’s actions, such as purchases, ratings (likes and dislikes), downloads, items searched for on a website and/or placed in a cart, and clicks on product links.")
    st.image("https://www.iteratorshq.com/wp-content/uploads/2021/06/content_based_collaborative_filtering.jpg")

#------------------------------

elif sidebar_option == "Content-based Filtering":
    st.header("Content-Based Filtering")
    st.image('img/tiki.jpg')
    # Explain the two types of recommendation systems
    st.write("<strong>Content-Based Filtering</strong> recommends products based on the accumulated knowledge of users. It consists of a resemblance between the items. The proximity and similarity of the product are measured based on the similar content of the item.", unsafe_allow_html=True)

    product_names = product_images['product_name'].tolist()

    # Add a search box for product name
    search_term = st.text_input('Enter a product name to search:', '')

    # Filter the product names based on the search term
    if search_term:
        product_names = [name for name in product_names if search_term.lower() in name.lower()]

    if len(product_names) == 0:
        st.write('No products found for the given search term ☹️')
    else:
        # Add a dropdown to select a product
        selected_product = st.selectbox('Select a product', product_names)

        # Get the recommendations for the selected product
        product_id_choose=item(selected_product)
        recommendations = content_based_product(int(product_id_choose))

        # Display the recommendations
        st.write(f'Top 10 products similar to {selected_product}:')
        img=img_cb(recommendations)
    
        #Adding recommend products when click
        click_id=recommendations['product_id'][recommendations['image']==img]
        st.write("---"*40)
        st.write("Recommend products for the item is clicking:")
        product_ID_input= click_id.iloc[0]
        additional_recommendations=content_based_product(product_ID_input).head(4)
        cols = st.columns(4)
        for j, additional_row in additional_recommendations.iterrows():
            with cols[j % 4]:
                st.image(additional_row['image'], width=None)
                st.write(additional_row['product_name'])


#####################
elif sidebar_option == "Collaborative Filtering":
    st.header("Collaborative Filtering")
    st.image('https://datamahadev.com/wp-content/uploads/2020/10/Recommender-System-datamahadev.png')
    st.write("<strong>Collaborative Filtering</strong> recommends products based on based on the user's historical choices. It focuses on relationships between the item and users; items’ similarity is determined by their rating given by customers who rated both the items.", unsafe_allow_html=True)
    #Load all unique customer_id by Grid
    gd_reviews= GridOptionsBuilder.from_dataframe(customer_id_lst)
    gd_reviews.configure_pagination(enabled=True)
    gd_reviews.configure_default_column(editable=False, groupable=True,enableValue=True,enableRowGroup=True)
    gd_reviews.configure_side_bar()

    sel_mode = 'multiple'
    gd_reviews.configure_selection(selection_mode=sel_mode, use_checkbox=True)
    gridoptions_reviews = gd_reviews.build()
    grid_table_reviews = AgGrid(customer_id_lst, gridOptions=gridoptions_reviews,
                            enable_enterprise_modules=True,
                            update_mode=GridUpdateMode.SELECTION_CHANGED | GridUpdateMode.VALUE_CHANGED| GridUpdateMode.MODEL_CHANGED,
                            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
                            header_checkbox_selection_filtered_only=True,
                            height=500,
                            allow_unsafe_jscode=True,
                            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                            reload_data=True,
                            fit_columns_on_grid_load=False
                            )

    sel_row_reviews = grid_table_reviews["selected_rows"]
            
    if sel_row_reviews!=[]:
        df_selected = pd.DataFrame(sel_row_reviews)
        df_selected=df_selected.drop("_selectedRowNodeInfo",axis=1)
        st.dataframe(df_selected)

        for i,row in df_selected.iterrows():
            customer_ID_input= row['customer_id']
            # Get the top recommended products for the customer
            lines = df[df['customer_id'] == customer_ID_input]
            als_recommend(lines)
