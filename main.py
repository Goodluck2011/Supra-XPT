from flask import Flask, request, render_template_string, session
import requests
import os

app = Flask(__name__)
app.secret_key = "secret_key"

API_KEY = "AIzaSyBuK7djAWyzf0zYFKKJRXRh_XTQsjNapQE"

def ask_ai(question):

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    data = {
        "contents": [{
            "role": "user",
            "parts": [{"text": question}]
        }]
    }

    try:
        res = requests.post(url, json=data)
        result = res.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "Error getting response"


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Chat</title>
<style>
body {font-family:Arial;background:#111;color:white;text-align:center;}
.chat {max-width:700px;margin:auto;}
.msg {padding:10px;margin:10px;border-radius:10px;}
.user {background:#1e88e5;text-align:right;}
.bot {background:#333;}
</style>
</head>
<body>

<div class="chat">
<h2>🤖 Gemini ChatBot</h2>

{% for msg in chat %}
<div class="msg {{msg.role}}">{{msg.text}}</div>
{% endfor %}

<form method="POST">
<input name="question" style="padding:10px;width:70%;" placeholder="Ask anything..." required>
<button style="padding:10px;">Send</button>
</form>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if "chat" not in session:
        session["chat"] = []

    if request.method == "POST":
        q = request.form["question"]
        answer = ask_ai(q)

        session["chat"].append({"role": "user", "text": q})
        session["chat"].append({"role": "bot", "text": answer})
        session.modified = True

    return render_template_string(HTML, chat=session["chat"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)