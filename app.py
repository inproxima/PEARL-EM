import streamlit as st 
from st_pages import Page, show_pages, add_page_title, Section, add_indentation

#page config
st.set_page_config(page_title="PEARL-PE: Persona Emulating Adaptive Research and Learning Bot (Program Evaluation Version)", page_icon="🤖", layout = "wide", initial_sidebar_state="expanded")
hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#add_page_title()
#add_indentation()
# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Section(name = "Menu", icon ="👇"),
        Page("pages/1_case.py", "Case 1"),
        Page("pages/2_case.py", "Case 2 "),
        Page("pages/3_case.py", "Case 3 "),
        Page("pages/4_case.py", "Case 4 "),
        Page("pages/5_case.py", "Case 5 "),
        
    ]
    )

#Main app
def main():
    st.title("Hi! I'm PEARL 👋")
    st.subheader("Persona Emulating Adaptive Research and Learning Bot")
    st.info("Program Evaluation Version")
    st.markdown("""___""")
    st.write("🤖 Hello, my name is PEARL. I am an AI program designed to simulate a particular persona and engage in conversations with humans. My purpose is to assist researchers in conducting interviews and gathering insights on reseach foci. I am constantly learning and adapting to new situations, so feel free to ask the persona you give me anything related to the research topic.")
    st.divider()

    st.title("Learning Task 2: Option 2")
    st.write("This option, LT#2, involves completing one of five available incomplete program evaluations using an innovative artificial intelligence program for data collection and analysis. This AI program is configured to simulate the personas of relevant program stakeholders who have participated in each hypothetical program. Each persona has reached a hypothetical conclusion after participating in the program. There are four personas available for each case. Each team will design interview questions and conduct interviews with these AI personas to collect essential data for their chosen evaluation. Click on the case from the sidebar to begin the interview.")
    
    st.subheader("Case Titles:")
    st.markdown("""

    - Case 1: Assessing the Impact of Mindfulness Training Programs on Teacher Stress Levels and Job Satisfaction: A Case Study

    - Case 2: Impact of Culturally Responsive Teaching Strategies on K-12 Teachers' Professional Development

    - Case 3: Evaluating the Role of Anti-Bias Training in Shaping Teachers' Attitudes and Behaviors: An Inclusive School Perspective

    - Case 4: Evaluating the Impact of AI Literacy Training on K-12 Teachers’ Assessment Strategies: A Case Study

    - Case 5: An Analysis of Leadership Development Programs for School Principals in the K-12 System
    
    """)

    st.markdown("___")
    st.info("This application, version dated June 14th, was developed by [Soroush Sabbaghan](ssabbagh@ucalgary.ca). It is powered by: [Streamlit](https://streamlit.io/), [Langchian](https://python.langchain.com/en/latest/index.html), and [ChatGPT API](https://openai.com/product), with the aim of supporting educational objectives. This work is released under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).")


if __name__ == '__main__':
	main()