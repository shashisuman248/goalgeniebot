from flask import Flask, request, send_file
from twilio.twiml.messaging_response import MessagingResponse
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

@app.route("/whatsapp/webhook", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "goal" in incoming_msg:
        # Create a simple PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 750, "GoalGenieBot Report")
        p.drawString(100, 730, f"Message: {incoming_msg}")
        p.save()
        buffer.seek(0)

        # Save file temporarily
        with open("goal_report.pdf", "wb") as f:
            f.write(buffer.read())
        buffer.seek(0)

        msg.body("Here is your PDF report.")
        msg.media("https://goalgeniebot-india.onrender.com/static/goal_report.pdf")
    else:
        msg.body("This is GoalGenieBot powered by Sip Wealth.")

    return str(resp)

@app.route("/")
def home():
    return "GoalGenieBot is running!"

if __name__ == "__main__":
    app.run(debug=True)
