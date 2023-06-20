import pandas as pd
import streamlit as st

from streamlit_chat import message
# For the chatbot type experience

import os
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
import json


def add_bg_from_url():
    st.markdown(
        f"""

         <style>
         .stApp {{
             background-image: url("https://png.pngtree.com/background/20210714/original/pngtree-abstract-low-poly-white-gold-line-background-picture-image_1235447.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )
add_bg_from_url()
st.header('File Info ChatBot')
st.subheader('(Credit: Mayur #OpenAI)')

with open("api_key.json", 'r') as f:
    json_data = json.load(f)
    os.environ["OPENAI_API_KEY"] = json_data['OPEN_API_Key']
    #os.environ["SERPAPI_API_KEY"] = json_data['SERP_API_Key']

# using session variables to store the chat history
# If this particular key is not present in this session_state, then create this generated key
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# AI output will be saved here

if 'past' not in st.session_state:
    st.session_state['past'] = []

# To clear text area after hitting Enter (after input provided by user)
def clear_text_input():
    global input_text
    input_text = ""
def get_text():
    global input_text
    input_text = st.text_input("Ask your questions!!", key="input", on_change=clear_text_input())
    return input_text

def get_file(file_data):
    if '.csv' in file_data.name:
        df = pd.read_csv(file_data)
    else:
        df = pd.read_excel(file_data)
    return df

# Create a file uploader
uploaded_file = st.file_uploader("Choose a file")
user_input = get_text()

# Use this file uploader, put it inside the agent (line4), it will work on this file and give the answer.

if uploaded_file:
    dataframe = get_file(uploaded_file)

    #Create the agent and start reading file with this agent
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), dataframe, verbose=True)

if st.button("Post"):
    with st.spinner("waiting for the response..."):
        if user_input:
            output = agent.run(user_input)

            # whenever new question asked using the agent, we'll take the response
            # & put it into these two variables
            st.session_state.past.append(user_input)
            st.session_state.generated.append(output)

if 'generated' in st.session_state:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
