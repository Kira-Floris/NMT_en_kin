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

from norvig import correction

def translate(req):
    res = requests.post(api_url, json=req)
    res = json.loads(res.text)
    return res['translation']

def correct(text):
    words = text.split(' ')
    correction_list = []
    for word in words:
        correct = correction(word)
        correction_list.append(correct[0])
    correction_text = ' '.join(correction_list)
    return correction_text

def form(src, trg, spellchecker=False):
    with st.form('Translate'):
        text = st.text_input("Enter text: ")
        submit = st.form_submit_button('Translate')
        if submit:
            if spellchecker:
                text_ = correct(text)
                st.subheader('Corrected text')
                st.code(text_)
                
                req = {
                    "src": src,
                    "trg": trg,
                    "text": text_
                } 
            else:
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
    checker = st.checkbox(label='Koresha SpellChecker', value=True)
    form('kin', 'en', checker)
    pass