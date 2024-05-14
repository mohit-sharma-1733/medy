import google.generativeai as genai
import PIL.Image
class GenerativeModelSetup:
    def __init__(self):
        # Configure API key
        genai.configure(api_key={API_KEY})

        # Set up the model
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    def start_conversation(self):
        convo = self.model.start_chat(history=[])
        return convo


    def validate_input_using_ai(self,input,image):
        convo = self.model.start_chat(history=[])
        image_text = f"whether the following text {input}" if not input[1] else f"Check this image {input[1]} and whether the following text {input[0]}"
#         prompt = f'''whether the following image  {image} is most likely related to the healthcare domain?

# * It mentions a body part, symptom, illness, or medical procedure. (e.g., headache, fever, surgery)
# * It refers to a medical professional, medication, or treatment. (e.g., doctor, nurse, prescription)
# * It discusses health advice, diagnosis, or prevention. (e.g., how to lower blood pressure, healthy diet)
# * It uses medical terminology or abbreviations commonly used in the healthcare field. (e.g., EKG, MRI, BP,medicine)

# Please consider all of these factors and provide a strictly not any other text just binary classification (True/False).
# '''     
#         prompt = f'''**If an image is uploaded:**

# 1. Use a pre-trained image classification model to classify the uploaded image. Commonly used models include:
#     * **Vision API:** https://cloud.google.com/vision
#     * **Cloud Healthcare API - AutoML Vision:** https://cloud.google.com/healthcare-api (Requires specific setup)
# 2. If the image classification model predicts a healthcare-related category (e.g., X-ray, medical equipment, medication) with high confidence, proceed to step 3. Otherwise, ignore the image and rely solely on the text prompt.

# **For both Text and (if applicable) Classified Image:**

# Whether the following combination of text and image is most likely related to the healthcare domain?

# **Text:**
# {input[0]}

# **Image:** {"" if not input[1] else input[1]} (If uploaded, describe the content briefly based on the classification model output, e.g., "An X-ray of a chest")

# Please consider all of these factors and provide a strictly not any other text just binary classification (True/False).
# '''
        #print(prompt)
        prompt = f"""
Check the text {input if input else ""} (if available) and image {image if image else ""} (if available) if they are related to healthcare ,then give appropriate response in humanized text and if not, then just give a text that it is not related to healthcare.
        """
        conversation = convo.send_message([prompt])
        print(conversation.text)
        return conversation.text
def main():
    model_setup = GenerativeModelSetup()
    conversation = model_setup.start_conversation()
    prompt = f"""
Check the text {input if input else ""} (if available) and image (if available) if they are related to healthcare ,then give appropriate response  in humanized text but don't write like 'this image is... and all' and if not, then just give a text that it is not related to healthcare.
        """
    message = [prompt, PIL.Image.open('rashes.jpg')]
    res = conversation.send_message(message)
    print(res)
    # result = model_setup.generate_content([
    # "what is in this image:", PIL.Image.open('image.png')])
    # print(result)
    # message = input("Enter your message:")
    # #message = "Can you process images using this model?"
    # res = conversation.send_message(message)
    # print(res.text)
    #print(conversation.last.text)

if __name__ == "__main__":
    main()
