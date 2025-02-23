import os
import json
import google.generativeai as gen_ai
from PIL import Image

#get working directory
working_directory=os.path.dirname(os.path.abspath(os.path.abspath(__file__)))

#Appending the config file path
config_file_path=f"{working_directory}/config.json"
config_data=json.load(open(config_file_path))

#loading api key
GOOGLE_API_KEY=config_data['GOOGLE_API_KEY']

#configure google.generativeai with the api key
gen_ai.configure(api_key=GOOGLE_API_KEY)

#function to load the gemini pro model
def load_gemini_pro_model():
    gemini_pro_model=gen_ai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# function for image captioning
def gemini_pro_vision_response(prompt, image):
    # load the model
    gemini_pro_vision_model = gen_ai.GenerativeModel("gemini-1.5-flash")
    # get the response
    response = gemini_pro_vision_model.generate_content([prompt, image])
    result = response.text
    return result

# image = Image.open("cat.jpg")
# prompt = "write a caption for this image"
# output = gemini_pro_vision_response(prompt, image)
# print(output)

#function to get embedded text
def embedded_model_response(input_text):
    embedded_model="models/embedding-001"
    embedding = gen_ai.embed_content(model=embedded_model,
                                     content=input_text,
                                     task_type="retrieval_document")
    embedding_list=embedding["embedding"]
    return embedding_list

output = embedded_model_response("Who is Virat Kohli?")
print(output)


#ask me anything
def gemini_pro_response(user_input):
    gemini_pro_model=gen_ai.GenerativeModel("gemini-pro")
    response=gemini_pro_model.generate_content(user_input)
    result=response.text
    return result

