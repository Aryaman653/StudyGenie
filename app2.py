import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMMathChain, LLMChain
from langchain.agents.agent_types import AgentType
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents import Tool, initialize_agent
from langchain.document_loaders import PyPDFLoader,YoutubeLoader
from langchain.callbacks import StreamlitCallbackHandler
from dotenv import load_dotenv
import validators
import os
from pypdf import PdfReader

# Define PDF extraction function for a single file
def extract_text_from_pdf(uploaded_file):
    temp_pdf = "./temp.pdf" 
    # Save uploaded file content to a temporary file
    with open(temp_pdf, "wb") as file:
        file.write(uploaded_file.getvalue())
    # Load the PDF content
    loader = PyPDFLoader(temp_pdf)
    docs = loader.load()  # Extract text or documents
    return docs  # Return extracted documents

# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="StudyGenie",page_icon="📖")
st.title("StudyGenie 👀🧠⚡️")
st.subheader("""
StudyGenie: Your Ultimate Study Assistant for Summarizing, Explaining, and Generating Practice Materials!

- **Summarizing Notes**: Automatically summarize your uploaded PDFs for easy revision.
- **Explaining Concepts**: Receive detailed, easy-to-understand explanations of complex topics.
- **Generating Practice Questions**: Generate multiple-choice, statement-based, and assertion-reasoning questions for self-assessment.
- **Flashcards**: Create flashcards for better retention and quick review.
- **Study Plans**: Get personalized study schedules tailored to your time and topics.
- **YouTube Notes**: Generate detailed notes from YouTube videos for better comprehension.
- **Essay Generation**: Receive a comprehensive essay on any topic, adhering to word limits and formatting.
""")



# Setup the sidebar
groq_api_key = st.sidebar.text_input("Enter Your Groq API key", type="password")
if not groq_api_key:
    st.warning("Please Enter API key to proceed!")
    st.stop()

uploaded_file = st.sidebar.file_uploader("Upload Only PDF files", type='PDF')

# Setup the llm model
llm = ChatGroq(api_key=groq_api_key, model_name="Gemma2-9b-It")

# Create the tools
#################################################################################
# 2. Summary Tool
t_2 = """
You are an agent for providing detailed-consise summaries of the given text.
text:{text}
"""
prompt_summary = PromptTemplate(input_variables=['text'], template=t_2)
summary_chain = LLMChain(llm=llm, prompt=prompt_summary)

#################################################################################
# 3. Explanation Tool
t_3 = """
You are an agent for providing detailed explanation of the given text in 200 words.
text:{text}
"""
prompt_explain = PromptTemplate(input_variables=['text'], template=t_3)
explain_chain = LLMChain(llm=llm, prompt=prompt_explain)

#################################################################################
# 4. QuestionMCQ Tool
t_4 = """
Generate 10 well-structured multiple-choice questions on the following topic. Each question should have exactly 4 options formatted as:

a) Option 1  
b) Option 2  
c) Option 3  
d) Option 4  

Provide the correct answers for all questions at the end.

Topic: {text}
"""

prompt_question1 = PromptTemplate(input_variables=['text'], template=t_4)
question_chain1 = LLMChain(llm=llm, prompt=prompt_question1)

#################################################################################
# 4. QuestionGenerate Tool
t_5 = """
Generate 10 good questions for the following topics each question should test the fundamentals of the topic. Also provide the answers to the questions at the end:
text:{text}
"""
prompt_question2 = PromptTemplate(input_variables=['text'], template=t_5)
question_chain2 = LLMChain(llm=llm, prompt=prompt_question2)
#################################################################################
t_6 = """
Generate 5 good Assertion-Reasoning type questions for the following topic:
topic:{text}

Each question should be in the following format:

1. **Assertion (A):** Write the assertion statement.
   **Reason (R):** Write the reasoning statement.

   - (a) Both A and R are true, and R is the correct explanation of A.
   - (b) Both A and R are true, but R is NOT the correct explanation of A.
   - (c) A is true, but R is false.
   - (d) A is false, but R is true.

Provide the correct option (a, b, c, or d) for each question at the end.
"""
prompt_question3 = PromptTemplate(input_variables=['text'], template=t_6)
question_chain3 = LLMChain(llm=llm, prompt=prompt_question3)
#################################################################################

# Flashcards Generator Tool
t_flashcards = """
Generate 10 flashcards based on the following content. Each flashcard should be in this format:

Question: <question>
Answer: <answer>

Content: {text}
"""
prompt_flashcards = PromptTemplate(input_variables=['text'], template=t_flashcards)
flashcards_chain = LLMChain(llm=llm, prompt=prompt_flashcards)

#################################################################################
#Generate study plan
study_plan_prompt = """
Generate a study plan for the following topic. The user will study for the specified number of hours, and the plan should include a breakdown of topics to study with estimated time for each section.

Topic: {text}
Total Study Time: {study_time} hours
"""
study_plan_template = PromptTemplate(input_variables=["text", "study_time"], template=study_plan_prompt)
study_plan_chain = LLMChain(llm=llm, prompt=study_plan_template)

#################################################################################
#Generate Video Summary
video_temp = """
summarize the following content
content: {text}.

Provide detailed notes that include the following:

Introduction: A brief overview of the contents's topic, main objective, and context.
Key Concepts: A thorough explanation of the core ideas and concepts discussed, with any relevant definitions or background information.
Important Details: Include any facts, statistics, or examples shared in the video that help clarify or support the main points.
Steps/Processes: If applicable, describe any steps, procedures, or methodologies mentioned in the video, breaking them down clearly.
Conclusion: Summarize any conclusions, key takeaways, or lessons learned from the video.
Visuals/Examples: Mention any notable visuals or examples (if relevant) that help illustrate the points being made.
Ensure the notes are comprehensive, well-organized, and easy to follow, with a focus on accuracy and clarity.
"""
video_prompt = PromptTemplate(input_variables=['text'], template=video_temp)
video_chain=LLMChain(llm=llm,prompt=video_prompt)

#################################################################################
#Generate Essay
essay_temp = """
Generate an essay on the following topic. The essay should be well-organized and comprehensive, including a unique title and the following sections:

Topic: {text}
word limit:{word_limit}
adhere to the specified word limit
Essay Sections:
1. Title: Provide a unique and creative title that reflects the essence of the topic.
2. Introduction: Write a brief introduction with an overview of the topic and its significance.
3. Key Concepts: Discuss the core concepts and ideas related to the topic with explanations and relevant definitions.
4. Main Body: Divide the body into sections, each focusing on a specific aspect of the topic, supported by facts, examples, or evidence.
5. Conclusion: Summarize the key points and offer a concluding thought or reflection.

Ensure that the essay is clear, coherent, and uses formal language. Provide accurate and well-structured arguments for each section.
"""
essay_prompt=PromptTemplate(input_variables=['text','word_limit'],template=essay_temp)
essay_chain=LLMChain(llm=llm,prompt=essay_prompt)

#################################################################################

# Initialize messages correctly in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! 👀 I am your personal study assistant, StudyGenie. How can I help you today? 😊"}
    ]

# Display all messages correctly
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

# Choose one option
st.write("Please Choose one of the following options:")
task = st.selectbox("What would you like to do?", ["Summarize Notes","Write Essay", "Explain Concept", "Generate Practice Questions-MCQ", "Generate Practice Questions-Statements","Generate Assestion-Reasoning Questions","Generate Flashcards","Generate Study Planner","Generate Notes From YouTube Video"])
user_input = st.text_input("Enter Your question here",placeholder="Ex: Newtons Laws Of Motion")
youtube_url = st.text_input("YouTube URL", placeholder="Enter YouTube URL")
study_time_input = st.number_input("Total Study Time (Only for study planner)",step=1)
word_limit = st.number_input("Total Word Limit(only for Essay)",step=1)
submitted = st.button("Let's Start")

if submitted:
    if task == "Explain Concept":
        if user_input:
            with st.spinner("✨ Analysing..."):
                st.chat_message("user").write(task)
                response = explain_chain.run(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)
        else:
            st.warning("Please Enter Topic")


    if task == "Write Essay":
        if not user_input or not word_limit:
            st.warning("Please enter the topic and word limit")
        else:
            with st.spinner("✨ Generating the essay..."):
                st.chat_message("user").write(task)
                response = essay_chain.run({"text":user_input,"word_limit":word_limit})
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)

    elif task == "Generate Practice Questions-MCQ":
        if user_input:
            with st.spinner("✨ Generating MCQ practice questions..."):
                st.chat_message("user").write(task)
                response = question_chain1.run(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)
        else:
            st.warning("Please Enter Topic")


    elif task == "Generate Practice Questions-Statements":
        if user_input:
            st.chat_message("user").write(task)
            with st.spinner("✨ Generating statement practice questions..."):
                response = question_chain2.run(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response) 
        else:
            st.warning("Please Enter Topic")

    elif task =="Generate Assestion-Reasoning Questions":
        if user_input:
            with st.spinner("✨ Generating MCQ practice questions..."):
                st.chat_message("user").write(task)
                response = question_chain3.run(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)
        else:
            st.warning("Please Enter Topic")

    elif task == "Generate Flashcards":
        if user_input:
            with st.spinner("✨📖 Generating Flashcards..."):
                st.chat_message("user").write(task)
                response = flashcards_chain.run(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response) 
        else:
            st.warning("Please Enter Topic")

    elif task == "Generate Study Planner":
        if study_time_input and user_input:
            with st.spinner("✨📖 Generating Personalized plan..."):
                # Input for study time
                st.chat_message("user").write(task)
                response = study_plan_chain.run({"text":user_input,"study_time":study_time_input})
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)
        else:
            st.warning("Please Enter Topics and Study Time(hrs)")

    elif task == "Summarize Notes":
        st.chat_message("user").write(task)
        if not uploaded_file:
            st.warning("Please upload the PDF")
        if uploaded_file:
            with st.spinner("✨ Summarizing Notes..."):
                # Call the function directly with the single uploaded file
                pdf_text = extract_text_from_pdf(uploaded_file)
                response = summary_chain.run(pdf_text)
                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.success(response)

    elif task == "Generate Notes From YouTube Video":
        if youtube_url:
            if not validators.url(youtube_url):
                st.error("Please provide a valid YouTube URL")
            else:
                try:
                    with st.spinner("✨Generating Notes..."):
                        loader=YoutubeLoader.from_youtube_url(youtube_url)
                        docs=loader.load()
                        response=video_chain.run(docs)
                        #Load the thumbnail:
                        video_id=youtube_url.split('=')[1]
                        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",use_container_width=True)
                        st.success(response)
                except Exception as e:
                    st.exception(f"Exception: {e}")
        else:
            st.warning("Please Enter YouTube video link")
