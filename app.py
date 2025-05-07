from flask import Flask, request, jsonify, render_template
from chatbot import ask_chatbot

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    
    if not user_input:
        return jsonify({"response": "Please enter a valid message"}), 400
    
    response = ask_chatbot(user_input)
    clean_res = response.replace('```', '').strip()
    # return jsonify({"response": response})
    return jsonify({"response": clean_res})

if __name__ == "__main__":
    app.run(debug=True)