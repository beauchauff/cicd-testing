"""
Streamlit Monitoring Dashboard
Reads and parses the prediction_logs.json for data drift analysis, target drift analysis, and model accuracy
and user feedback.
"""
import streamlit as st
import json
import pandas as pd
import os
import plotly.figure_factory as ff


#app layout
st.title('Movie Review Sentiment Monitoring Dashboard')
st.write('Checking for data drift, target drift, and model accuracy')

#Load dataset function
@st.cache_data
def load_imdb():
    df = pd.read_csv("IMDB Dataset.csv")
    df["text_length"] = df["review"].astype(str).apply(len)
    return df

#Load and parse file from /logs directory function
@st.cache_data
def load_logs():
    df_path = "../logs/prediction_logs.json"
    if not os.path.exists(df_path):
        return pd.DataFrame()

    with open (df_path, "r") as f:
        lines = f.readlines()

    data= [json.loads(line) for line in lines]
    df = pd.DataFrame(data)
    df["text_length"] = df["text"].astype(str).apply(len)
    return df

# Load data to streamlit for use
train_df = load_imdb()
log_df = load_logs()

#histogram data grouped
st.subheader("Data Drift Analysis - Review length histogram")
hist_data= [train_df["text_length"], log_df["text_length"]]
group_labels = ["IMDB review length", "Logged review length"]

fig = ff.create_distplot(hist_data, group_labels, bin_size=10)
st.plotly_chart(fig)

#Target Drift Analysis
st.subheader("Target Drift - Comparing Predictions to User Feedback Setniment")

col1, col2, = st.columns(2)

with col1:
    st.write("User Feedback Sentiment")
    st.bar_chart(log_df["true_sentiment"].value_counts())

with col2:
    st.write("Predicted Sentiment")
    st.bar_chart(log_df["predicted_sentiment"].value_counts())

#Model Accuracy & User Feedback
st.subheader("Performance Metrics")

correct = (log_df["true_sentiment"] == log_df["predicted_sentiment"]).sum()
total = len(log_df)
accuracy = correct/total

pred_pos = log_df[log_df["predicted_sentiment"] == "positive"]
true_pos = pred_pos[pred_pos["true_sentiment"] == "positive"]
precision = len(true_pos) / len(pred_pos) if len(pred_pos) > 0 else 0.0

st.metric("Accuracy", f"{accuracy:.2%}")
st.metric("Precision (Positive Class)", f"{precision:.2%}")

#Warning for accuracy <80%

if accuracy < 0.80:
    st.error("Model performance has dropped to less than 80%")

