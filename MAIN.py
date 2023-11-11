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
    num_subtitles = st.number_input("Enter the number of subtitles", min_value=1, max_value=20, value=1)
    
    content_list = []
    
    # Ingreso de contenido para subtítulos
    st.write("Enter content for each subtitle:")
    for i in range(num_subtitles):
        content = st.text_area(f"Content for Subtitle {i+1}")
        content_list.append(content)
        
    prompt = '\n\n'.join(content_list)  # Unir todos los bloques de contenido
    
    word_count = st.number_input("Enter the desired word count for the essay")
else:
    st.warning("Open the sidebar and enter your OpenAI API key")

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# Generar subtítulos automáticamente
def generate_subtitles(content):
    paragraphs = content.split('\n\n')
    subtitles = []
    
    for paragraph in paragraphs:
        # Generar subtítulo para cada párrafo usando el inicio del contenido
        subtitle = paragraph[:50] if len(paragraph) > 50 else paragraph
        subtitles.append(subtitle)
    
    return subtitles

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

# Generar subtítulos y ensayo
if prompt and API:
    suggested_subtitles = generate_subtitles(prompt)
    st.write("Suggested Subtitles:")
    for i, subtitle in enumerate(suggested_subtitles):
        approved = st.checkbox(f"Approve Subtitle {i+1}: {subtitle}")
        if not approved:
            new_subtitle = st.text_input("Enter new subtitle:")
            suggested_subtitles[i] = new_subtitle if new_subtitle else subtitle
    
    st.write("Approved Subtitles:")
    for i, subtitle in enumerate(suggested_subtitles):
        st.write(f"Subtitle {i+1}: {subtitle}")
    
    revised_prompt = '\n\n'.join(suggested_subtitles)
    
    generated_essay = ""
    while True:
        essay = essay_chain.run(revised_prompt + generated_essay)
        word_count = len(essay.split())
        if word_count > word_count:
            break
        generated_essay = essay
    
    final_essay = " ".join(essay.split()[:word_count])
    
    st.write("Generated Essay:")
    st.write(final_essay)
