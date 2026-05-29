import streamlit as st
import os
from groq import Groq
import fitz
st.title("PDF Chatbot")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # 2. Define where to save the file
    save_path = os.path.join("uploads", uploaded_file.name)
    
    # 3. Create the folder if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
        
    # 4. Write the file to your disk
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Document UPLOADED: {uploaded_file.name}")

# Open PDF
if uploaded_file is not None:
  reader = fitz.open(save_path)

# Extract text from all pages
  text = ""
  for page in reader:
    text += page.get_text()
# Chat Box
  messages = st.container(height=400)
  if prompt := st.chat_input("How can I help you?"):
      messages.chat_message("user").write(prompt)
# Initialize the Groq client
      client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
      )
# Create a chat completion
      chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"You are given 2 parameters, text and prompt. Text is the file which contains the content and prompt is the instruction or the questions of user answer them polietly and be very clear. Make sure the questions asked to you are from or related to the file or the given content or else just say I don't know in a formal way: {text} ,{prompt}",
                
            }
        ],
        model="llama-3.3-70b-versatile",
        max_tokens=500,
      )
# Display the assistant's response
      messages.chat_message("assistant").write(chat_completion.choices[0].message.content)
