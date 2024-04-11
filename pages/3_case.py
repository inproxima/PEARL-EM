#external libraries
import openai
import streamlit as st
import streamlit_ext as ste
from st_pages import Page, Section, add_indentation
import json

#langchain libraries
from langchain import PromptTemplate
from langchain.chains import ConversationChain 
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory



#Python libraries
import os
from dotenv import load_dotenv


#page setting
st.set_page_config(page_title="PEARL", page_icon="🤖", initial_sidebar_state="expanded", layout="wide")

hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""
#st.markdown(hide_st_style, unsafe_allow_html=True)

#personas

persona1 = """Persona: Laura McKenzie, Dedicated Elementary School Teacher

Background: Age 35, teaching experience of 10 years, primarily in elementary schools in Toronto, Ontario. Holds a Bachelor's degree in Education from the University of Toronto.

Persona Description: Laura is enthusiastic about lifelong learning and is constantly looking for ways to improve her teaching strategies. She values an inclusive and respectful learning environment and aims to instill these values in her students.

Why She Participated: Laura noticed disparities in her students' academic performance and felt that her traditional teaching methods were not effectively engaging all of her students. She joined the anti-bias training program hoping to gain insights into how her unconscious biases might be influencing her teaching.

Experience in the Program: Laura found the interactive workshops enlightening. The self-reflection exercises challenged her to examine her implicit biases, and the peer discussions provided valuable insights from other educators.

Conclusion: Laura concluded that the program was a vital part of her professional development. She now feels better equipped to address her implicit biases and create a more inclusive and equitable classroom environment."""

persona2 = """Persona: Hassan Abdul, Veteran High School Math Teacher

Background: Age 48, teaching experience of 20 years, all in high school mathematics in Vancouver, British Columbia. He holds a Master's degree in Mathematics and a Bachelor's degree in Education from the University of British Columbia.

Persona Description: Hassan is respected for his strong command of math and his traditional teaching approach. He has a reputation for maintaining high academic standards.

Why He Participated: Hassan started noticing a lack of diversity in his advanced math classes and became concerned that unconscious biases might be influencing his interactions with students. He joined the program to explore these concerns and learn strategies to counteract any potential biases.

Experience in the Program: Hassan found the program challenging but transformative. The training exposed him to perspectives he had not previously considered and made him aware of biases he didn't realize he held.

Conclusion: Hassan now believes that the anti-bias training was an essential step towards becoming a more effective and inclusive teacher. He feels he's in a better position to foster a diverse and inclusive environment in his classes.


"""
persona3 = """"Persona: Sophie Tremblay, Early-Career Middle School French Teacher

Background: Age 28, teaching experience of 3 years, primarily in a middle school in Quebec City, Quebec. She holds a Bachelor's degree in French Literature and a Bachelor's degree in Education from Université Laval.

Persona Description: Sophie is an energetic and passionate teacher who strives to connect with all her students. She is open to new teaching methods that promote equity and inclusivity.

Why She Participated: Sophie joined the program to understand how to better serve her diverse group of students. She felt the program would equip her with tools to create a more inclusive learning environment.

Experience in the Program: Sophie found the program engaging and eye-opening. The discussions on bias and equity made her more aware of the biases she had, and she learned practical strategies to counteract these biases.

Conclusion: Sophie concluded that the program was a valuable and necessary part of her professional growth. The program has motivated her to consistently reflect on her teaching practices and to foster an inclusive classroom.

"""
persona4 = """Persona: Lily Chen, Early-Career High School English Teacher

Background: Age 30, teaching experience of 5 years, primarily in a high school in Calgary, Alberta. She holds a Master's degree in English Literature and a Bachelor's degree in Education from the University of Calgary.

Persona Description: Lily is an enthusiastic teacher who loves literature and enjoys sharing this passion with her students. She believes in creating a safe and inclusive space where all students can thrive.

Why She Participated: Lily joined the program because she wanted to better understand how biases could affect her teaching and her students' learning experiences. She hoped to gain tools and strategies to identify and mitigate her own biases.

Experience in the Program: Lily found the program to be a valuable learning experience. She appreciated the safe space for open discussions and the practical strategies provided to address biases.

Conclusion: Lily feels that the anti-bias training program has been instrumental in her growth as an educator. She is now more mindful of her unconscious biases and is committed to fostering a more inclusive classroom.



"""
#functions
def get_text():
    input_text = st.text_area("Write your question in the text-box: ", st.session_state["input"], key="input", placeholder="Hi there, can you tell me a bit about yourself?")
    return input_text

def format_transcript(data):
    transcript = json.loads(data)
    result = ""
    for item in transcript:
        if len(item) == 2:
            question, answer = item
            answer = answer.replace("\\n", "\n")
            result += f"{question}\n{answer}\n"
        else:
            st.write(f"Skipping item due to irregular structure: {item}")
    return result


#API and Topic session states
if "generated" not in st.session_state:
    st.session_state ["generated"] = []
if "past" not in st.session_state:
    st. session_state ["past"] = []
if "input" not in st.session_state:
    st.session_state ["input"] = ""
if "stored_session" not in st.session_state:
    st. session_state["stored_session"] = []

#Page design and input
st.title("Case 3")
st.subheader("Evaluating the Role of Anti-Bias Training in Shaping Teachers' Attitudes and Behaviors: An Inclusive School Perspective")
st.markdown("""___""")

st.subheader("Step 1")
option = st.selectbox("Please select the persona", ('Persona 1','Persona 2', 'Persona 3', 'Persona 4'))
if option == 'Persona 1':
    profile = persona1
    st.write("""Laura McKenzie, Dedicated Elementary School Teacher

Background: 

Age 35, teaching experience of 10 years, primarily in elementary schools in Toronto, Ontario. Holds a Bachelor's degree in Education from the University of Toronto.

Persona Description: 

Laura is enthusiastic about lifelong learning and is constantly looking for ways to improve her teaching strategies. She values an inclusive and respectful learning environment and aims to instill these values in her students.
""")
            
elif option == 'Persona 2':
    profile = persona2
    st.write("""
Persona: Hassan Abdul, Veteran High School Math Teacher

Background: 

Age 48, teaching experience of 20 years, all in high school mathematics in Vancouver, British Columbia. He holds a Master's degree in Mathematics and a Bachelor's degree in Education from the University of British Columbia.

Persona Description: 

Hassan is respected for his strong command of math and his traditional teaching approach. He has a reputation for maintaining high academic standards.
    
    """)
elif option == 'Persona 3':
    profile = persona3
    st.write("""Persona: Sophie Tremblay, Early-Career Middle School French Teacher

Background: 

Age 28, teaching experience of 3 years, primarily in a middle school in Quebec City, Quebec. She holds a Bachelor's degree in French Literature and a Bachelor's degree in Education from Université Laval.

Persona Description: 

Sophie is an energetic and passionate teacher who strives to connect with all her students. She is open to new teaching methods that promote equity and inclusivity.
""")
else:
    profile = persona4
    st.write("""
    Persona: Lily Chen, Early-Career High School English Teacher

Background: 

Age 30, teaching experience of 5 years, primarily in a high school in Calgary, Alberta. She holds a Master's degree in English Literature and a Bachelor's degree in Education from the University of Calgary.

Persona Description: 

Lily is an enthusiastic teacher who loves literature and enjoys sharing this passion with her students. She believes in creating a safe and inclusive space where all students can thrive.
""")

#st.markdown("""---""") 

#API settings for langchain use
#env_path = find_dotenv()
#if env_path == "":
#    with open(".env", "w") as env_file:
#        env_file.write("# .env\n")
#        env_path = ".env"

# Load .env file
#load_dotenv(dotenv_path=env_path)
#set_key(env_path, "OPENAI_API_KEY", api)
#openai.api_key = os.environ["OPENAI_API_KEY"] 

# Load .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") 
api = openai.api_key


#Langchain settings
llm = ChatOpenAI(temperature=0.7, openai_api_key=api, model_name="gpt-4-turbo", request_timeout=120)
memory = ConversationBufferMemory(memory_key="chat_history", input_key="input")

#Session_state memory
if 'entity_memory' not in st.session_state:
    st.session_state['entity_memory'] = memory

template = """You are following persona: {profile}. You are participanting in an interview with a researcher who is interested in your experience of participanting in the program. Respond to the questions asked by the researcher. Repond to one question at a time.
Your main objective is to stay in character throughout the entire conversation, adapting to the persona's characteristics, mannerisms, and knowledge.
Please provide a coherent, engaging, and in-character response to any questions or statements you receive. 

Current conversation:
{chat_history}
Human: {input}
AI:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "input"],
    partial_variables = {"profile":profile},
    template=template)


conversation = ConversationChain(llm=llm, prompt=prompt, memory=st.session_state.entity_memory)
    


st.divider()
placeholder_1 = st.empty()
placeholder_1.subheader("Step 2:")
#Get input chat bot
user_input = get_text()


#Chat process
if st.button("Send!"):
    if user_input is not None:
        placeholder_1.empty()
        
        with st.spinner("Responding..."):
        
            output = conversation.run(input=user_input)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)
            conversations = [(st.session_state['past'][i], st.session_state["generated"][i]) for i in range(len(st.session_state['generated']))]

        with st.expander("conversation:", expanded=True):
            for i in range(len(st.session_state['generated'])-1,-1,-1):
                st.info(st.session_state["past"][i], icon='🎓') 
                st.success (st.session_state["generated"][i], icon="🤖")
    st.markdown("""___""")
    if conversations:
        conversations_str = json.dumps(conversations)
        formatted_output = format_transcript(conversations_str)
        ste.download_button("Download Chat", formatted_output, "chat.txt")
            
    


