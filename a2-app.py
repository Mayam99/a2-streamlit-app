import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting up the Streamlit app
st.title("Personal Finance Dashboard")
st.sidebar.header("Upload Your Data")
st.sidebar.write("Upload your bank statement in CSV format.")

# File upload widget
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['csv'])

# Load the sample data if no file is uploaded
if uploaded_file:
    data = pd.read_csv(uploaded_file)
else:
    data = pd.read_csv("transactions.csv")
    st.info("Using sample data. Upload your CSV file to use your data.")

# Display the first few rows of the data
st.subheader("Transaction Data")
st.write(data.head())

# Data preprocessing
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.to_period('M')

# Sidebar filters
categories = st.sidebar.multiselect("Filter by Category", options=data['Category'].unique())
if categories:
    data = data[data['Category'].isin(categories)]

# Aggregations for insights
monthly_summary = data.groupby('Month').sum(numeric_only=True)['Amount'].reset_index()

# Display Insights
st.subheader("Monthly Expenses and Income Overview")
st.line_chart(monthly_summary, x='Month', y='Amount')

# Categorization of expenses and income
expenses = data[data['Amount'] < 0]
income = data[data['Amount'] > 0]

# Budget tracking
st.subheader("Expense Breakdown")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=expenses, x='Category', y='Amount', ax=ax, ci=None)
ax.set_title('Expenses by Category')
st.pyplot(fig)

# Financial goal setting
st.sidebar.subheader("Set Your Financial Goals")
goal_amount = st.sidebar.number_input("Goal Amount", min_value=0, value=1000)
current_savings = income['Amount'].sum()
goal_progress = min((current_savings / goal_amount) * 100, 100)
st.sidebar.write(f"Current Savings: ${current_savings:.2f}")
st.sidebar.progress(goal_progress / 100)

# Spending habit insights
st.subheader("Spending Insights")
if goal_progress < 100:
    st.write("You're on track! Keep saving to reach your goal.")
else:
    st.write("Congratulations! You've reached your financial goal.")

# Customizable widgets
st.sidebar.subheader("Customize Dashboard")
show_income_chart = st.sidebar.checkbox("Show Income Chart", value=True)

if show_income_chart:
    st.subheader("Income Breakdown")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=income, x='Category', y='Amount', ax=ax, ci=None)
    ax.set_title('Income by Category')
    st.pyplot(fig)
