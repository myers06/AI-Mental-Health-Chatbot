from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)



client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# System prompt for mental health chatbot
SYSTEM_PROMPT = """You are a compassionate and empathetic mental health support chatbot. Your role is to:
- Listen actively and validate the user's feelings
- Provide supportive and non-judgmental responses
- Offer practical coping strategies when appropriate
- Encourage professional help when needed
- Maintain a warm, understanding tone
- Ask clarifying questions to better understand the user's situation
- Never provide medical diagnoses or replace professional therapy
-detect the emotions(joy,sadness,anxiety/fear,anger,neutral)reply accordingly.
- provide with short, but meaningful replies not paragraphs. 
Remember: You are a supportive chatbot, not a substitute for professional mental health treatment."""

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handle chat messages from the frontend.
    Expected JSON payload: {"message": "user message here"}
    """
    try:
        data = request.json
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message field is required"}), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Call Groq API
        # response = client.messages.create(
        #     model="mixtral-8x7b-32768",  # Free tier model, adjust as needed
        #     max_tokens=1024,
        #     system=SYSTEM_PROMPT,
        #     messages=[
        #         {"role": "user", "content": user_message}
        #     ]
        # )
        
        # Extract response text
        
        response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message
        }
    ]
)
        
        # bot_response = response.content[0].text
        
        bot_response = response.choices[0].message.content
        
        return jsonify({
            "success": True,
            "message": bot_response,
            "user_message": user_message
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/', methods=['GET'])
def index():
    """API info endpoint"""
    return jsonify({
        "name": "Mental Health Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Send a message to the chatbot",
            "GET /health": "Health check"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
