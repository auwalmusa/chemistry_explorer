import streamlit as st
import openai
import numpy as np
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie  # Ensure this import is done correctly
# Set the OpenAI API key using the secret
openai.api_key = st.secrets["openai"]["api_key"]

st.set_page_config(page_title="Chemistry Explorer 🧪", page_icon=":microscope:", layout='wide')
# Function to load Lottie animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        return None
# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        menu_title=None,  # If you want to add a title, you can do it here.
        options=["Home", "Example", "Quiz", "Periodic Table", "Exam Prep", "Topic Assistance"],
        icons=['house', 'book', 'clipboard-check', 'table', 'trophy', 'question-circle'],  # Changed 'graduation-cap' to 'book'
        menu_icon="cast",  # This is the icon for the menu itself, visible when the menu is collapsed.
        default_index=0  # "Home" page is the default selection.
    )

# Define a function to show a Lottie animation for correct answers
def show_correct_answer_animation():
    correct_answer_lottie_url = "https://drive.google.com/uc?export=view&id=1CgISKhtdj8U-BmUdn3HoVyPF81e84aT_"  # Use a working URL
    correct_answer_animation = load_lottieurl(correct_answer_lottie_url)
    if correct_answer_animation:
        st_lottie(correct_answer_animation, height=200, key="correct_answer")

# Add to the options list in the sidebar navigation
options=["Home", "Example", "Quiz", "Periodic Table", "A-Level Exam Prep", "Topic Assistance"]

# Handle A-Level Exam Prep
if selected == "Exam Prep":
    st.header("Chemistry Exam Preparation")
    user_input = st.text_input("Enter the topic you're preparing for (e.g., Reaction Mechanisms):")
    if user_input and st.button("Generate Quiz for Exam Prep"):
        quiz_content = generate_quiz(user_input)
        st.markdown(quiz_content)

# Handle Topic Assistance
if selected == "Topic Assistance":
    st.header("Chemistry Topic Assistance")
    user_input = st.text_input("Describe what you're struggling with (e.g., balancing chemical equations):")
    if user_input and st.button("Help Me Understand"):
        explanation_content = generate_explanation(user_input)
        st.markdown(explanation_content)

# Load a Lottie animation for the main screen
lottie_url = "https://drive.google.com/uc?export=view&id=1f74XhctB0aLJHYwxnPk9I7P4Eh-E9J4a"
lottie_animation = load_lottieurl(lottie_url)

# Create columns for the title and animation
col1, col2 = st.columns([2, 3])  # Adjust the ratio as needed
with col1:
    st.title("Chemistry Explorer 🧪")
    st.write("***Your Personal Revision Guide***")

with col2:
    if lottie_animation:
        st_lottie(lottie_animation, height=300, key="chemistry")

# Handling "Periodic Table" selection
if selected == "Periodic Table":
    st.header("Periodic Table of Elements")
    # Providing a clickable link to the Periodic Table
    st.markdown("""
        Visit the interactive [Periodic Table of Elements](https://ptable.com/) on PTable.
        """, unsafe_allow_html=True)

# Functions for generating content with OpenAI
def generate_explanation(topic):
    prompt = f"As a Professional Chemist, explain the concept of {topic} in simple terms and using analogies, suitable for A-level students. Keep the explanation concise, under 300 words. Also, suggest a reading from Lister, T & Renshaw, J (2008) AQA Chemistry."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        temperature=0.5,
    )
    explanation = response.choices[0].text.strip()
    return explanation + "\n\n**Recommended Reading:** Lister, T & Renshaw, J (2008) AQA Chemistry As/A2 Nelson Thornes ISBN 978-0-19-835181-8 (As) & 978-0-19-835771-1 (A2)."
def generate_detailed_explanation(description):
    prompt = f"Explain in detail for A-level Chemistry students: {description}. Provide a clear, step-by-step explanation to help understand the concept, including any relevant examples or diagrams."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=750,  # Adjusted for detailed explanations
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )
    detailed_explanation = response.choices[0].text.strip()
    return detailed_explanation

def generate_example(topic):
    prompt = f"Provide a simple example illustrating the chemistry topic: {topic}, suitable for A-level students. Include a problem statement and a solution. Keep it under 300 words."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        temperature=0.5,
    )
    example = response.choices[0].text.strip()
    return example

def generate_quiz(topic):
    prompt = f"Generate an interactive quiz question for A-level students on the topic of {topic}, including multiple choices and indicating the correct answer. Provide a brief explanation for the correct answer."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=300,
        temperature=0.7,
    )
    quiz_question = response.choices[0].text.strip()
    return quiz_question
# Define your chemistry topics
topics = [
    "Atomic Structure", "Structure and Bonding", "Periodicity","Ideal Gas Equation", "Stoichiometry",
    "Energetics", "Acid-Base Reactions","Oxidation, reduction, and redox reactions",
    "Kinetics", "Chemical Reactions and Equilibria", "Organic Chemistry",
    "Health, Safety, and Good Practice in the Laboratory"
]
def format_as_bullets(explanation):
    """Converts an explanation into a bulleted Markdown list"""
    lines = explanation.splitlines()
    bullet_list = "\n".join(["* " + line for line in lines if line])
    return bullet_list

# Page Content Based on Selection
if selected == "Home":
    topic = st.selectbox("**Select a module topic:**", ["Select a topic"] + topics)
    if topic and topic != "Select a topic":
        explanation = generate_explanation(topic)
        bulleted_explanation = format_as_bullets(explanation)
        st.markdown(explanation)

elif selected == "Example":
    topic = st.selectbox("Select a module topic to see an example:", ["Select a topic"] + topics)
    if topic and topic != "Select a topic":
        example = generate_example(topic)
        st.write(example)
elif selected == "Quiz":
    topic = st.selectbox("Select a module topic to take a quiz on:", ["Select a topic"] + topics)
    if topic and topic != "Select a topic":
        quiz_question = generate_quiz(topic)
        st.write(quiz_question)

        # Prompt for user answer moved inside the 'if' block to ensure proper indentation
        user_answer = st.text_input("Enter your answer (e.g., A, B, C, D):").strip().upper()

        if st.button("Submit Answer"):
            correct_answer_line = next((line for line in quiz_question.split('\n') if "Correct answer:" in line or "Correct Answer:" in line), None)
            if correct_answer_line:
                correct_answer = correct_answer_line.split(":")[1].strip().upper()

                if user_answer == correct_answer:
                    st.success("Correct! 🎉")
                    show_correct_answer_animation()  # Show animation if the answer is correct
                else:
                    st.error("Oops! That's not correct. Try again.")
            else:
                st.error("Couldn't find the correct answer. Please check the question format.")

