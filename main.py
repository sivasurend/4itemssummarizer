import streamlit as st
import openai

# Function to initialize OpenAI with the API key
def init_openai(api_key):
    openai.api_key = api_key

# Function to summarize text using OpenAI's GPT-4 chat model
def summarize_text(article, instructions, max_words):
    # Convert max_words to max_tokens (approximately 4 tokens per word)
    max_tokens = max_words * 4

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an intelligent text summarizer.\n\nI will provide you a source article. And I will provide you instructions. You need to generate the output based on the instructions I provide.\n\n"
            },
            {
                "role": "user",
                "content": f"Article - {article}\nInstruction - {instructions}\n\nGenerate the output in not more than {max_words} words"
            }
        ],
        temperature=0.7,
        max_tokens=max_tokens,
        top_p=0.3,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    return response.choices[0].message['content']

st.image('./Lyzr Logo 250px by 250px.png')

# Streamlit app layout
st.title('The 4 Items Summarizer by Lyzr.ai')

# Input for OpenAI API Key
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Text window for article input
article = st.text_area("Paste your article here (up to 2000 words)", height=300, max_chars=2000)

# Text window for custom requirements
instructions = st.text_area("Enter your custom requirements (up to 100 words)", height=100, max_chars=100)

# Input for desired output word count
output_word_count = st.number_input("Enter the desired word count for the summary", min_value=10, max_value=500, value=100, step=10)

# Submit button for summarization
if st.button('Summarize'):
    if api_key and article and instructions:
        init_openai(api_key)
        summary = summarize_text(article, instructions, output_word_count)
        st.write(summary)
    else:
        st.error("Please fill in all the fields.")
