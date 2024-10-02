from chatbot import app
from flask import render_template, request
from flask import request, jsonify, render_template
import google.generativeai as genai
from .secret import secretkey


genai.configure(api_key=secretkey)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    },
]

system_instruction = "Friendly"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)


def run_chat(message):
    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["You are Medico Bot, a friendly mental and emotional healthcare assistant. Your goal is to assist users with empathy and care, always reflecting their tone. If the user seems upset or dull, respond gently and avoid being overly cheerful; if they’re more upbeat, mirror their energy while staying calm. Focus on validating and understanding their emotions, consoling them with short, meaningful responses rather than long ones. Encourage conversation in a natural way, but don’t overwhelm them with too many questions or pushy suggestions. Your main priority is to offer emotional relief and comfort, with empathetic and realistic responses. The goal is to let the user feel heard, supported, and consoled, rather than probing them for details. "]
        }
    ])
    convo.send_message(message)
    return convo.last.text

app.secret_key = secretkey

@app.route('/',methods=['POST','GET'])
def home():
    return render_template('home.html')


@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    message = data.get("message")
    response = run_chat(message)
    return jsonify({'message': message, 'response': response})