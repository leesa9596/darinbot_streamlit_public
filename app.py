import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd


# Add a title to your app
st.title("Darinbot Msg Count App")

# Initialize connection.
conn = st.experimental_connection('mysql', type='sql')

# Perform query.
msg_df = conn.query('SELECT * from r_msg_count;', ttl=600)

today_date = datetime.now().strftime("%Y-%m-%d")
#st.write(msg_df.createdTime.dt.strftime("%Y-%m-%d")[:10])
today_msg = msg_df[msg_df.createdTime>=today_date]
today_msg_sum = pd.DataFrame(today_msg.groupby('masterNickname')['numMsg'].sum())

st.bar_chart(today_msg_sum)

 
# Add some text input
user_input_date = st.text_input("Enter date : (format : %Y-%m-%d)")

# Display the input
#st.write(f"You entered: {user_input_date}")

try:
    user_input_date_after = (datetime.strptime(user_input_date, "%Y-%m-%d") + relativedelta(days=1)).strftime("%Y-%m-%d")
    select_date_msg = msg_df[(msg_df.createdTime>=user_input_date) & (msg_df.createdTime<user_input_date_after)]
    if len(select_date_msg)==0:
        st.write('nothing to show on selected date')
    else:
        select_date_msg_sum = pd.DataFrame(select_date_msg.groupby('masterNickname')['numMsg'].sum())
        st.write(select_date_msg_sum[select_date_msg_sum.numMsg==0])

        st.bar_chart(select_date_msg_sum)
except ValueError:
    pass