#using Python3.11
import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
from PIL import Image

# page config
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

#dashboard setup
st.title("Real-Time / Live Data Science Dashboard")
st.title("Upload the Image")

# Upload image through Streamlit File Uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display the uploaded image
    # st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    # Optionally, you can perform some processing on the uploaded image here
    # For example, you can use PIL to resize or manipulate the image

    # Example: Resize the uploaded image to a fixed width
    img = Image.open(uploaded_image)
    st.subheader("Processed Image")
    st.image(img, caption="Processed Image", use_column_width=True)

job_filter = st.selectbox("select the job", pd.unique(df["job"]))
df = df[df["job"] == job_filter]
placeholder = st.empty()

#simulating data for real time feed
for seconds in range(200):
    df["age_new"] = df["age"] * np.random.choice(range(1, 5))
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))
    # time.sleep(1)
    # creating KPIs
    avg_age = np.mean(df["age_new"])

    count_married = int(
        df[(df["marital"] == "married")]["marital"].count()
        + np.random.choice(range(1, 30))
    )
    balance = np.mean(df["balance_new"])
    # creating a single-element container.
    with placeholder.container():
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age ⏳",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )

        kpi2.metric(
            label="Married Count 💍",
            value=int(count_married),
            delta=-10 + count_married,
        )

        kpi3.metric(
            label="A/C Balance ＄",
            value=f"$ {round(balance,2)} ",
            delta=-round(balance / count_married) * 100,
        )

        # Interactive charts
        fig_col1, fig_col2 = st.columns(2)

        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="age_new", x="marital"
            )
            st.write(fig)
        
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x="age_new")
            st.write(fig2)
        
        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)
