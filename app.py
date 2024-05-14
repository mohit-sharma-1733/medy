from flask import Flask, request, jsonify
from gemini import GenerativeModelSetup
import PIL.Image
from io import BytesIO
from flask_cors import CORS
from openai import OpenAI
import base64
import io
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)

OPENAI_KEY = os.getenv("OPEN_AI_SECRET_KEY")
client  = OpenAI(api_key=OPENAI_KEY)

# Prompt for GPT-3 model
PROMPT = """
Check the input message to determine if it is related to healthcare. 
If the input is about healthcare, provide a humanized response. 
Otherwise, prompt the user to ask a question related to healthcare. 
Ensure the response is informative and easy to understand.
But Please, don't ignore the greetings(give appropriate response for greetings)
"""

def generate_response(message, img=None):

    # Create the base message list with the user message
    user_content = [{"type": "text", "text": message}]

    if img:
        user_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{img}",
                "detail": "high"
            }
        })

    messages = [
        {
            "role": "user",
            "content": user_content
        }
    ]

    # Call the OpenAI API with the prepared messages
    print(f"MESSAGES:{messages}")
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages
    )

    # Return the response from the model
    return completion.choices[0].message.content


@app.route('/chat', methods=['POST'])
def chat():
    # try:
        data = request.form
        message = data.get('message')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400

        img = None
        image = None
        
        if 'image' in request.files:
            img = request.files.get('image')
            if img:
                try:
                    image_data = img.read()
                    image = base64.b64encode(image_data).decode('utf-8')
                except Exception as e:
                    return jsonify({'error': f'Failed to process the image. {str(e)}'}), 500

        response = generate_response(message, image)
        return jsonify({'response': response})

    # except Exception as e:
    #     return jsonify({'error': f'An unexpected error occurred. {str(e)}'}), 500


@app.route('/chat2', methods=['POST'])
def chat2():
    data = request.form
    message = data.get('message')
    img = ""
    if request.files.get("image"):
        img = PIL.Image.open(BytesIO(request.files.get('image').read()))
    #Image.open(BytesIO(img_file.read()))
    # Initialize GenerativeModelSetup
    model_setup = GenerativeModelSetup()
    prompt = f"""
Check the text {message if message else ""} (if available) and image (if available) if they are related to healthcare ,then give appropriate response with a basic medical advice  in humanized text but don't write like 'this image is... and all' and if not, then just give a text that it is not related to healthcare and also ask to rephrase the healthcare or personal care related text and please don't ignore greetings(if greetings are given please respond back appropriately).
        """
    conversation = model_setup.start_conversation()
    response = conversation.send_message([prompt,img] if img else prompt)

    return jsonify({'response': response.text})
    # else:
    #     return jsonify({'response':'Hmm... I am unable to answer this question as I am specially designed for healthcare related queries!'})

if __name__ == '__main__':
    app.run(debug=True)