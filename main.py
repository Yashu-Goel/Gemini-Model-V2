import os
from PIL import Image

import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import (load_gemini_pro_model, gemini_pro_vision_response, embedded_model_response, gemini_pro_response)

working_directory=os.path.dirname(os.path.abspath(__file__))
# print("Output: ")
# print(working_directory)
# print(os.path.abspath(__file__))


st.set_page_config(
    page_title="Chat with Gemini-Pro!",
    page_icon=":brain:",  # Favicon emoji #Use emojipedia for more emojis
    layout="centered",  # Page layout option
)

with st.sidebar:
    selected=option_menu("gemini AI",
                         ["ChatBot",
                          "Image Captioning",
                          "Embedded Text",
                          "Ask me anything"],
                          menu_icon='robot', icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill'],
                          default_index=0)
#For more icons: Refer: https://icons.getbootstrap.com/
    # print(selected)

#function to translate the user role for streamlit
def translate_role_for_streamlit(user_role):
    if user_role=='model':
        return 'assistant'
    else:
        return user_role
if selected=="ChatBot":
    model=load_gemini_pro_model()

    #initialize chat session in streamlit if not present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session=model.start_chat(history=[])

    #Streamlit page title
    st.title("🤖 Chatbot")
    #display the chat history
    print(st.session_state.chat_session.history)
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    #User input
    user_input=st.chat_input("Ask me anything...")
    if user_input:
        #add user input to the chat session
        st.chat_message("user").markdown(user_input)
        #get the response from the model
        gemini_response=st.session_state.chat_session.send_message(user_input)
        #display the response  
        with st.chat_message('assistant'):
            st.markdown(gemini_response.text)

#Image captioning Page
if selected=='Image Captioning':
    st.title("📸 Image Captioning")
    uploaded_image=st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
    if st.button("Generate Caption"):
        image=Image.open(uploaded_image)
        col1, col2=st.columns(2)
        with col1:
            resized_image=image.resize((800, 500))
            st.image(resized_image)
        default_prompt="write a caption for this image"

        #getting the response from gemini pro vision model
        caption=gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

if selected=="Embedded Text":
    st.title("📝 Embedded Text")
    input_text=st.text_area(label="", placeholder="Enter the text to embed")
    if st.button("Embed Text"):
        #get the response from the model
        response=embedded_model_response(input_text)
        st.markdown(response) 

#Ask me anything
if selected=="Ask me anything":
    st.title("❓ Ask me anything")
    user_input=st.text_area(label="", placeholder="Ask me anything...")
    if st.button("Get answer"):
        response=gemini_pro_response(user_input)
        st.markdown(response)