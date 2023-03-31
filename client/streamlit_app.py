import streamlit as st
import requests
import json

# page configurations
st.set_page_config(page_title='Machine Translation', page_icon=':tada:')
st.title("Machine Translation")
st.text('---------------------------------------')

sidebar = st.sidebar.selectbox(
    'What language would you like to translate from?',
    ('english to kinyarwanda', 'kinyarwanda to english')
)

api_url = 'http://localhost:8000/api/v1/translate'

def translate(req):
    res = requests.post(api_url, json=req)
    res = json.loads(res.text)
    return res['translation']

def form(src, trg):
    with st.form('Translate'):
        text = st.text_input("Enter text: ")
        submit = st.form_submit_button('Translate')
        if submit:
            req = {
                "src": src,
                "trg": trg,
                "text": text
            } 
            translation = translate(req)
            st.code(translation) 

if sidebar=='english to kinyarwanda':
    st.header('English to Kinyarwanda')
    form('en', 'kin')
    pass

elif sidebar=='kinyarwanda to english':
    st.header('Kinyarwanda to English')
    form('kin', 'en')
    pass