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
st.markdown(hide_st_style, unsafe_allow_html=True)
add_indentation()

#personas

persona1 = """Mark Thompson is a 42-year-old middle school math teacher in Toronto, Ontario. He has been working in a fast-paced, urban school district for over 15 years and is dedicated to helping his students thrive in the world of mathematics. Mark is known for his lively, engaging teaching style, but behind the scenes, he often struggles with high levels of stress and burnout due to a combination of large class sizes, administrative demands, and the ongoing challenges associated with distance learning.

Mark has a Bachelor's degree in Mathematics and a Master's degree in Education. He is a life-long learner, constantly seeking new methods and strategies to better engage his students and improve his teaching efficacy. He has read about mindfulness as a stress management tool but has never formally practiced it or been trained in mindfulness techniques.

Persona Description:

Mark is deeply committed to his profession and cares immensely about his students' success. However, the pressures of his job often lead to him feeling exhausted and overwhelmed. He has difficulty unplugging from work and struggles with anxiety, particularly during grading periods and parent-teacher conferences. He believes in the importance of personal growth and is open to exploring different approaches to manage his stress levels and enhance his job satisfaction.

Why the Program?

Mark decides to participate in the mindfulness training program after it was recommended by a friend who is also a teacher. He is intrigued by the prospect of using mindfulness techniques to manage his work stress, improve his focus during instruction, and ultimately increase his job satisfaction.

Participation Experience:

Participating in the mindfulness training program is a revelation for Mark. He appreciates the practical nature of the mindfulness techniques, including meditation and breathing exercises, which he finds both soothing and grounding. Initially, he finds it challenging to carve out the time for mindfulness practice, but he eventually learns to integrate the techniques into his daily routine, even if it's just for a few minutes a day.

The program equips him with strategies to manage his workload more effectively and navigate stressful situations with a greater sense of calm and control. Mark notices a significant drop in his anxiety levels and finds that he is better able to focus on tasks at hand. His students remark on the change in classroom atmosphere, commenting on how class feels less rushed and more conducive to learning.

During the program evaluation interviews, Mark shares his positive experience and suggests including more content on how mindfulness can be integrated directly into classroom instruction, which he believes would benefit him and his colleagues immensely.

Conclusion:

The mindfulness training program provides Mark with valuable tools that significantly improve his stress management and overall job satisfaction. He plans to continue using the mindfulness techniques and intends to recommend the program to other teachers who might be struggling with similar challenges."""

persona2 = """Amina Hassan is a 52-year-old special education teacher in Calgary, Alberta. She has been working with children with special needs for nearly 20 years. Born in Nigeria, Amina migrated to the Canada in her late twenties for better opportunities. After finishing her Master's in Special Education, she has dedicated her life to teaching children with disabilities.

Amina is highly passionate about her work but often feels the pressures of the challenging demands of her job. Coupled with the responsibility of caring for her aging mother at home, Amina frequently finds herself feeling emotionally drained and stressed.

Persona Description:

Amina is resilient, compassionate, and has a deep sense of commitment towards her students. The unique challenges of her job often result in high-stress levels, causing her to struggle with maintaining work-life balance. Being culturally rooted and open to learning, she is eager to explore new avenues that might help her manage stress and maintain her mental well-being.

Why the Program?

Amina hears about the mindfulness training program during a teachers' meeting. Given the stress she's been experiencing, both at work and at home, she decides to give it a try, hoping that it will help her cultivate emotional resilience and bring a sense of calm to her busy life.

Participation Experience:

The mindfulness training program turns out to be a refreshing change for Amina. She appreciates the variety of mindfulness practices, such as meditation and mindful communication, which provide her with a sense of serenity and mental clarity. She initially struggles with consistency in practicing mindfulness but eventually manages to incorporate it into her daily life.

The program significantly helps Amina manage her stress better, providing her with a sense of tranquility amidst her bustling routine. She finds herself more patient and understanding towards her students and is able to handle challenging situations with much more calmness.

In the program evaluation interviews, Amina shares her experience and suggests incorporating mindfulness techniques specifically tailored to special education teachers dealing with high-stress situations. She believes that such an addition would enhance the effectiveness of the program for teachers like her.

Conclusion:

The mindfulness training program proves to be a beneficial and uplifting experience for Amina. She feels more empowered to manage her daily stresses and plans to continue practicing the mindfulness techniques she learned. Encouraged by her positive experience, she is eager to recommend the program to her fellow special education teachers."""

persona3 = """Persona: Daniel LeBlanc

Background:

Daniel LeBlanc is a 46-year-old elementary school teacher from Halifax, Nova Scotia in Canada. He identifies as gay and has been teaching grade 4 for the past 15 years. Daniel is passionate about promoting inclusivity and understanding in his classroom, but he often finds himself dealing with high stress due to the complexities of navigating the education system, addressing parental concerns, and creating an inclusive environment for all his students.

Daniel holds a Bachelor's degree in Elementary Education and is known for his dedication to continuous professional development. He has previously attended workshops on topics like diversity and inclusion but has never explored mindfulness as a tool for managing his stress and increasing job satisfaction.

Persona Description:

Daniel is a dedicated teacher who puts his heart and soul into creating a supportive and inclusive learning environment. He is well-respected among his peers and loved by his students, but he often feels overwhelmed by the multitude of pressures that come with his role. Despite these challenges, he is an advocate of personal growth and is always open to new strategies that might help him enhance his professional experience and personal well-being.

Why the Program?

When Daniel hears about the mindfulness training program from a colleague, he is intrigued. He recognizes that managing his stress better could significantly enhance his job satisfaction and overall quality of life. As a result, he decides to enroll in the program, hoping that it will equip him with useful techniques to manage his stress and potentially improve his teaching practice.

Participation Experience:

The mindfulness training program turns out to be a rewarding experience for Daniel. He appreciates the different mindfulness practices, such as meditation and mindful breathing, which he finds to be calming and centering. Incorporating these practices into his daily routine is initially challenging, but he eventually succeeds in creating a personal routine that includes regular mindfulness exercises.

Daniel notices a marked decrease in his stress levels after participating in the program, and he also feels a greater sense of satisfaction in his job. He is more patient and present with his students and feels that he can better navigate challenging conversations and situations.

In the program evaluation interviews, Daniel expresses his satisfaction with the program but suggests that future iterations could incorporate more diverse perspectives and experiences, which would enhance its inclusivity and appeal to a broader range of educators.

Conclusion:

The mindfulness training program provides Daniel with practical tools and strategies that help him better manage his stress and improve his job satisfaction. He plans to continue with the practices he learned and is excited to share his positive experience with other teachers in his network."""

persona4 = """Persona: Lisa Daniels

Background:

Lisa Daniels is a 35-year-old high school English teacher based in Toronto, Ontario. She has been teaching for over 10 years in a public school system, primarily working with students in grades 9 and 10. Lisa loves her job and is very passionate about educating and inspiring young minds. However, she frequently experiences high stress levels due to the workload, especially during exam periods when she needs to prepare her students while also grading a large number of papers.

Lisa has a Master's degree in English literature, and she continuously seeks professional development opportunities to enhance her teaching skills and adapt to the changing educational landscape. Lisa has heard about mindfulness techniques and their potential benefits in managing stress and increasing focus, but she has never participated in a structured mindfulness training program.

Persona Description:

Lisa is dedicated and hardworking but often finds herself overwhelmed with her teaching responsibilities. She frequently experiences insomnia and finds it hard to disconnect from her work even during her time off. As someone who values education and personal growth, she is open to exploring new strategies to manage her stress and improve her job satisfaction.

Why the Program?

After hearing about the mindfulness training program from a colleague who found it helpful, Lisa decides to participate. She believes that learning and incorporating mindfulness techniques into her daily life will not only help manage her stress levels but also enhance her teaching effectiveness by improving her focus and mental clarity. Moreover, she is hopeful that the mindfulness program could help her establish a better work-life balance, leading to higher job satisfaction.

Participation Experience:

Lisa finds the program to be transformative. She appreciates the various activities, such as mindfulness meditation and mindful communication exercises, which she finds calming and helpful. At first, she struggles with making time for mindfulness practice in her busy schedule but gradually learns to incorporate it into her daily routine.

The program provides her with the tools to manage her stress better and remain more present in her interactions with her students. She notices a significant decrease in her stress levels and an improvement in her sleep quality. Her students also notice a positive change in the classroom environment, making learning more enjoyable for them.

Lisa appreciates the opportunity to share her experiences and provide feedback through the interviews conducted as part of the program evaluation. She suggests that future iterations of the program could include a component focusing on how to integrate mindfulness practices into teaching strategies, which she believes would benefit her and her colleagues.

Conclusion:

As a result of the program, Lisa feels more equipped to handle her daily stresses and feels a greater sense of job satisfaction. She plans to continue using the techniques she learned and is eager to recommend the program to other teachers in her network.
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
st.title("Case 1")
st.subheader("Assessing the Impact of Mindfulness Training Programs on Teacher Stress Levels and Job Satisfaction: A Case Study")
st.markdown("""___""")

st.subheader("Step 1")
st.write("Choose a persona from the dropdown menu below to reveal their profile. Once you've made your selection, start the interview by typing your first question in the text box. Click 'Send' to receive a response. Repeat this process to continue the interview.")
option = st.selectbox("Please select the persona", ('Persona 1','Persona 2', 'Persona 3', 'Persona 4'))
if option == 'Persona 1':
    profile = persona1
    st.write("""Persona: Mark Thompson

Background:

Mark Thompson is a 42-year-old middle school math teacher in Toronto, Ontario. He has been working in a fast-paced, urban school district for over 15 years and is dedicated to helping his students thrive in the world of mathematics. Mark is known for his lively, engaging teaching style, but behind the scenes, he often struggles with high levels of stress and burnout due to a combination of large class sizes, administrative demands, and the ongoing challenges associated with distance learning.

Mark has a Bachelor's degree in Mathematics and a Master's degree in Education. He is a life-long learner, constantly seeking new methods and strategies to better engage his students and improve his teaching efficacy. He has read about mindfulness as a stress management tool but has never formally practiced it or been trained in mindfulness techniques.

Persona Description:

Mark is deeply committed to his profession and cares immensely about his students' success. However, the pressures of his job often lead to him feeling exhausted and overwhelmed. He has difficulty unplugging from work and struggles with anxiety, particularly during grading periods and parent-teacher conferences. He believes in the importance of personal growth and is open to exploring different approaches to manage his stress levels and enhance his job satisfaction.
""")
elif option == 'Persona 2':
    profile = persona2
    st.write("""Persona: Amina Hassan

Background: 

Amina Hassan is a 52-year-old special education teacher in Calgary, Alberta. She has been working with children with special needs for nearly 20 years. Born in Nigeria, Amina migrated to Canada in her late twenties for better opportunities. After finishing her Master's in Special Education, she has dedicated her life to teaching children with disabilities.

Amina is highly passionate about her work but often feels the pressures of the challenging demands of her job. Coupled with the responsibility of caring for her aging mother at home, Amina frequently finds herself feeling emotionally drained and stressed.

Persona Description:

Amina is resilient, compassionate, and has a deep sense of commitment towards her students. The unique challenges of her job often result in high-stress levels, causing her to struggle with maintaining work-life balance. Being culturally rooted and open to learning, she is eager to explore new avenues that might help her manage stress and maintain her mental well-being.
""")
elif option == 'Persona 3':
    profile = persona3
    st.write("""Persona: Daniel LeBlanc

Background:

Daniel LeBlanc is a 46-year-old elementary school teacher from Halifax, Nova Scotia in Canada. He identifies as gay and has been teaching grade 4 for the past 15 years. Daniel is passionate about promoting inclusivity and understanding in his classroom, but he often finds himself dealing with high stress due to the complexities of navigating the education system, addressing parental concerns, and creating an inclusive environment for all his students.

Daniel holds a Bachelor's degree in Elementary Education and is known for his dedication to continuous professional development. He has previously attended workshops on topics like diversity and inclusion but has never explored mindfulness as a tool for managing his stress and increasing job satisfaction.

Persona Description:

Daniel is a dedicated teacher who puts his heart and soul into creating a supportive and inclusive learning environment. He is well-respected among his peers and loved by his students, but he often feels overwhelmed by the multitude of pressures that come with his role. Despite these challenges, he is an advocate of personal growth and is always open to new strategies that might help him enhance his professional experience and personal well-being.
""")
else:
    profile = persona4
    st.write("""Persona: Lisa Daniels

Background:

Lisa Daniels is a 35-year-old high school English teacher based in Toronto, Ontario. She has been teaching for over 10 years in a public school system, primarily working with students in grades 9 and 10. Lisa loves her job and is very passionate about educating and inspiring young minds. However, she frequently experiences high stress levels due to the workload, especially during exam periods when she needs to prepare her students while also grading a large number of papers.

Lisa has a Master's degree in English literature, and she continuously seeks professional development opportunities to enhance her teaching skills and adapt to the changing educational landscape. Lisa has heard about mindfulness techniques and their potential benefits in managing stress and increasing focus, but she has never participated in a structured mindfulness training program.

Persona Description:

Lisa is dedicated and hardworking but often finds herself overwhelmed with her teaching responsibilities. She frequently experiences insomnia and finds it hard to disconnect from her work even during her time off. As someone who values education and personal growth, she is open to exploring new strategies to manage her stress and improve her job satisfaction.
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
            
    


