import os 
import streamlit as st 

st.set_page_config(page_title='Essay Writer', layout='wide')

with st.sidebar:
    API = st.text_input("Enter Your OpenAI API", type="password")
    
    if API:
        st.balloons()
        
    st.text('Made by Muhammad Umer')
        
os.environ['OPENAI_API_KEY'] = API

# App framework
st.title('🔗 Essay Writer Bot Made using Langchain 🦜')
if API:
    subtitle_list = []
    content_list = []
    
    # Ingreso de subtítulos
    st.write("Enter nine subtitles:")
    for i in range(9):
        subtitle = st.text_input(f"Subtitle {i+1}")
        subtitle_list.append(subtitle)

    # Ingreso de contenido
    st.write("Enter content for each subtitle:")
    for subtitle in subtitle_list:
        content = st.text_area(f"Content for '{subtitle}'")
        content_list.append(content)
        
    prompt = '\n\n'.join([f"{sub}: {content}" for sub, content in zip(subtitle_list, content_list)])
else:
    st.warning("Open the sidebar and enter your OpenAI API key")

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Prompt template
essay_template = PromptTemplate(
    input_variables=['topic'],
    template='write an essay based on the following subtitles:\n{topic}'
)

# Memory
essay_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')

# LLMs
if API:
    llm = OpenAI(temperature=0.9) 
    essay_chain = LLMChain(llm=llm, prompt=essay_template, verbose=True, output_key='essay')

# Generación del ensayo
if prompt and API:
    essay = essay_chain.run(prompt)
    st.write(essay)
