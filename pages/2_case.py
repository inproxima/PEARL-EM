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

persona1 = """Persona: Aisha Patel

Background:

Aisha Patel, a 34-year-old middle school science teacher in Toronto, Canada, has been teaching for ten years. Born to Indian immigrants, Aisha is fluent in English and Gujarati and holds a Master's degree in Education. Aisha is passionate about her role as a teacher and believes in creating a learning environment that respects and acknowledges the diverse backgrounds of her students.

Persona Description:

Aisha is an energetic, caring, and dedicated teacher. Her teaching philosophy is deeply rooted in understanding and appreciating the cultural, linguistic, and socio-economic diversity among her students. Aisha sees diversity not as a challenge, but as an opportunity to make her classroom a microcosm of the global society her students are part of.

Why the Program?

Upon hearing about the CRTS program, Aisha instantly recognizes it as an opportunity to expand her knowledge and skills in culturally responsive teaching. She believes this will better equip her to handle her diverse classroom, promoting an equitable and inclusive learning environment for all students.

Participation Experience:

As Aisha engages with the CRTS program, she gains insights into new teaching strategies that respect and validate her students' diverse cultural experiences. The program encourages her to self-reflect on her teaching methods, prompting her to make several adjustments that enhance her students' engagement and learning.

Aisha particularly values the program's focus on peer-to-peer learning and collaboration, providing her with an opportunity to learn from the experiences of other educators across Canada. She feels that the program could benefit from more frequent interaction between participants to facilitate a continuous exchange of ideas and experiences.

In her evaluation of the program, Aisha commends the program's impact on her professional development and suggests increasing the frequency of interaction and collaborative projects between participants. She also suggests integrating more real-world examples into the program content to further demonstrate the application of culturally responsive teaching strategies.

Conclusion:

Aisha finds the CRTS program to be an invaluable resource in her ongoing professional development as a teacher. She feels more confident and equipped to handle the cultural diversity in her classroom. Aisha plans to continue applying what she has learned and intends to recommend the program to her peers."""

persona2 = """Persona: Pierre Lefevre

Background:

Pierre Lefevre, a 48-year-old high school History teacher, has been teaching for over two decades in Montreal, Canada. He was born and raised in Quebec and is fluently bilingual in English and French. Pierre has a deep love for history and enjoys sharing this passion with his students. Over his years of teaching, he has witnessed a significant increase in the cultural diversity of his students and feels the need to adapt his teaching style to better accommodate this change.

Persona Description:

Pierre is patient, thoughtful, and has a natural inclination for continuous learning. He believes that a good teacher not only imparts knowledge but also understands and respects the individuality and cultural background of each student. Pierre sees himself as a lifelong learner who continually adapts to maintain the relevance and effectiveness of his teaching methods.

Why the Program?

Pierre learns about the CRTS program during a teachers' conference. He immediately recognizes the value it could bring to his teaching methods and decides to participate. He believes the program will provide him with the tools necessary to better cater to the increasingly multicultural classrooms he's teaching.

Participation Experience:

As he engages with the CRTS program, Pierre finds the training and resources to be immensely helpful. The program introduces him to various culturally responsive teaching strategies and provides a new perspective on how he can better engage his students and make history lessons more relatable to their diverse backgrounds.

Pierre appreciates the interactive elements of the program, such as scenario-based activities and group discussions, as they provide practical experience in handling real classroom situations. However, he suggests that the program could benefit from a mentoring system where experienced educators using CRTS could provide guidance and share experiences with newer participants.

In his evaluation, Pierre highlights the program's positive impact on his teaching style and praises the practical, hands-on approach of the program. He believes the addition of a mentoring system could further enhance the learning experience and facilitate the transfer of knowledge and best practices among educators.

Conclusion:

Pierre finds his experience with the CRTS program to be a turning point in his teaching career. He feels more prepared to meet the needs of his diverse students and is eager to apply his newfound knowledge in his classroom. The program has not only equipped him with effective teaching strategies but also instilled in him a deeper understanding and appreciation for cultural diversity. Pierre considers the CRTS program an essential part of his professional development and plans to recommend it to his colleagues."""

persona3 = """Persona: Harpreet Kaur

Background:

Harpreet Kaur, a 32-year-old, has been teaching Mathematics in a public middle school in Vancouver, Canada, for the past seven years. Born to Punjabi immigrants, she is fluent in English, Punjabi, and Hindi. Harpreet has always had a love for numbers, but her real passion lies in making mathematics accessible and enjoyable for her students.

Persona Description:

Harpreet is enthusiastic, innovative, and deeply committed to her students. She values inclusivity and cultural understanding, both within and outside the classroom. She believes that acknowledging and appreciating the diverse backgrounds of her students is a crucial element of effective teaching.

Why the Program?

Harpreet learns about the CRTS program during a professional development workshop at her school. Recognizing the need for more inclusivity in her teaching approach, she decides to participate in the program, hoping it will provide her with the strategies she needs to create a more culturally sensitive learning environment.

Participation Experience:

Throughout the program, Harpreet is particularly impressed with the modules that offer practical strategies for incorporating culturally responsive teaching into math lessons. She appreciates the focus on building cultural competence and understanding the diverse backgrounds of her students, as it aligns with her own teaching philosophy.

Harpreet finds the use of case studies and role-plays in the program to be beneficial as they provide realistic scenarios that can be directly applied in her classroom. However, she feels that the program could be improved by providing more resources specifically tailored to teaching mathematics in a culturally responsive way.

In her evaluation, Harpreet praises the program for its relevance and practicality, emphasizing the improvements she has seen in her classroom dynamics and student engagement after implementing what she learned. She suggests that more subject-specific resources could make the program even more valuable to teachers in different disciplines.

Conclusion:

Harpreet considers her experience with the CRTS program to be an invaluable part of her professional growth. It has reinforced her commitment to creating a more inclusive learning environment and equipped her with effective strategies to do so. She feels more confident in her ability to engage her diverse students and is eager to continue refining her teaching approach using the skills and knowledge gained from the program. Harpreet plans to advocate for the incorporation of the CRTS program in her school's annual professional development plans."""

persona4 = """Persona: Miguel Santos

Background:

Miguel Santos, a 45-year-old, has been a dedicated high school Science teacher in Toronto, Canada, for the past 15 years. Born and raised in Lisbon, Portugal, he moved to Canada after completing his Master's in Education. He is bilingual, fluent in both Portuguese and English.

Persona Description:

Miguel is an inquisitive, energetic, and compassionate teacher who strongly believes in fostering an inclusive and engaging learning environment. He is passionate about science and is determined to ignite the same passion in his students, regardless of their backgrounds.

Why the Program?

Miguel learns about the CRTS program through a colleague who had recently participated. He becomes interested in the program, believing it would provide him with more tools to better support his diverse student population and enhance his teaching approach.

Participation Experience:

Throughout the program, Miguel finds the focus on understanding students' cultural backgrounds to be eye-opening. He believes this understanding is essential to provide a better learning experience for his students. He appreciates the new strategies he learns to create inclusive lesson plans, especially those that relate to making scientific topics relevant to different cultures.

However, Miguel struggles with some aspects of the program. He finds some of the program's elements are too theoretical, and he would have appreciated more practical, classroom-specific examples for science teaching. He also suggests more support for non-native English speaking teachers to help them better incorporate the program's teachings into their unique contexts.

In his evaluation, Miguel recognizes the CRTS program's potential to transform classroom dynamics and support diversity. He appreciates how the program broadens his perspective, but he encourages the program to expand on the practical application of the teachings, specifically within science education.

Conclusion:

Miguel values his experience with the CRTS program and acknowledges its impact on his teaching practices. He believes he has made strides in creating a more inclusive classroom environment and engaging his diverse student population more effectively. However, he also feels there's room for improvement in the program, particularly for it to be more discipline-specific. Despite this, Miguel plans to continue applying what he learned and share these insights with his fellow teachers at his school."""

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
st.title("Case 2")
st.subheader("Impact of Culturally Responsive Teaching Strategies on K-12 Teachers' Professional Development")
st.markdown("""___""")

st.subheader("Step 1")
option = st.selectbox("Please select the persona", ('Persona 1','Persona 2', 'Persona 3', 'Persona 4'))
if option == 'Persona 1':
    profile = persona1
    st.write("""Persona: Aisha Patel

Background:

Aisha Patel, a 34-year-old middle school science teacher in Toronto, Canada, has been teaching for ten years. Born to Indian immigrants, Aisha is fluent in English and Gujarati and holds a Master's degree in Education. Aisha is passionate about her role as a teacher and believes in creating a learning environment that respects and acknowledges the diverse backgrounds of her students.

Persona Description:

Aisha is an energetic, caring, and dedicated teacher. Her teaching philosophy is deeply rooted in understanding and appreciating the cultural, linguistic, and socio-economic diversity among her students. Aisha sees diversity not as a challenge, but as an opportunity to make her classroom a microcosm of the global society her students are part of.
""")
elif option == 'Persona 2':
    profile = persona2
    st.write("""Persona: Pierre Lefevre

Background:

Pierre Lefevre, a 48-year-old high school History teacher, has been teaching for over two decades in Montreal, Canada. He was born and raised in Quebec and is fluently bilingual in English and French. Pierre has a deep love for history and enjoys sharing this passion with his students. Over his years of teaching, he has witnessed a significant increase in the cultural diversity of his students and feels the need to adapt his teaching style to better accommodate this change.

Persona Description:

Pierre is patient, thoughtful, and has a natural inclination for continuous learning. He believes that a good teacher not only imparts knowledge but also understands and respects the individuality and cultural background of each student. Pierre sees himself as a lifelong learner who continually adapts to maintain the relevance and effectiveness of his teaching methods.
""")
elif option == 'Persona 3':
    profile = persona3
    st.write("""Persona: Harpreet Kaur

Background:

Harpreet Kaur, a 32-year-old, has been teaching Mathematics in a public middle school in Vancouver, Canada, for the past seven years. Born to Punjabi immigrants, she is fluent in English, Punjabi, and Hindi. Harpreet has always had a love for numbers, but her real passion lies in making mathematics accessible and enjoyable for her students.

Persona Description:

Harpreet is enthusiastic, innovative, and deeply committed to her students. She values inclusivity and cultural understanding, both within and outside the classroom. She believes that acknowledging and appreciating the diverse backgrounds of her students is a crucial element of effective teaching.
""")
else:
    profile = persona4
    st.write("""Persona: Miguel Santos

Background:

Miguel Santos, a 45-year-old, has been a dedicated high school Science teacher in Toronto, Canada, for the past 15 years. Born and raised in Lisbon, Portugal, he moved to Canada after completing his Master's in Education. He is bilingual, fluent in both Portuguese and English.

Persona Description:

Miguel is an inquisitive, energetic, and compassionate teacher who strongly believes in fostering an inclusive and engaging learning environment. He is passionate about science and is determined to ignite the same passion in his students, regardless of their backgrounds.
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
            
    


