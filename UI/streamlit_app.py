import streamlit as st 
import pandas as pd
import time
import requests
import os
from pathlib import Path
from dotenv import load_dotenv 

load_dotenv(dotenv_path=Path('.') / '.env')


def flatten(lst):
    return [l for ls in lst for l in ls]

algorithm = st.sidebar.selectbox("algorithm", ["basic"])
print(algorithm)

if "selection" not in st.session_state:
        st.session_state["selection"] = [[]]
        
def get_records(products, lst):
    r = [p for p in products if p["product_name"] in lst]
    return r

def get_pids(records):
    return [p["product_id"] for p in records]

def update_selection(options, selections, new=False):
    if new:
        st.session_state["selection"].append(get_records(options, selections))
    else:
        st.session_state["selection"][-1] = get_records(options, selections)

text = st.text_input("search products to choose from options below")
st.session_state["text"] = text 
response = [] if not text else requests.get(f"{os.getenv('API')}/search/{text}").json()

with st.form("my_form"):
    options = [c["product_name"] for c in response]    
    selections = st.multiselect(
        'Choose products added to your basket',
        options
    )
    # Every form must have a submit button.
    submitted = st.form_submit_button("Add/update basket")



if "prevText" not in st.session_state or st.session_state["prevText"] != st.session_state["text"]:
    update_selection(response, selections, new=True)
    st.session_state["prevText"] = st.session_state["text"] 
else:
    update_selection(response, selections, new=False)

if len(flatten(st.session_state["selection"])) > 0:
    selected_records = flatten(st.session_state["selection"])
    st.write('You selected:', pd.DataFrame.from_records(selected_records)[["product_id", "product_name", "department"]])
    run = st.button('get recommendations')
    if run:
        with st.spinner('Getting recommendations ...'):
            with st.echo():
                recommandations = requests.get(f"{os.getenv('API')}/recommend/{algorithm}", params={"q":get_pids(selected_records)}).json()["products"]
            st.success("recommendations retrieved")
            st.write(pd.DataFrame.from_records(recommandations))
    