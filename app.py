import os
import sys
from flask import Flask, request
from pymessenger import Bot
from handleInput import response

app = Flask(__name__)

PAGE_ACCESS_TOKEN ="EAAE4QQuoY1gBAMmPHL2VtfFjeo2qSVFplJiy5bupeQYlgZB3KpJ53fv0kt2iYmcQGiwmyKAYTPSKNuOVtccAihJmLPfQqMzKyPuo3D1H6gQcobKTOFMcfeDCCn0ZBZCM4ZCU46Oyo8bM8ZBxjKiNQHAuiH0gpR151iGQSDoxaggZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "123456789":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Successfully :)", 200

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] =='page':
        for entry in data['entry']:
            for messaging_event in entry ['messaging']:
                
                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    messaging_text = messaging_event["message"]["text"] 
                    
                    responses = response(messaging_text)
                    bot.send_text_message(sender_id, responses)

    return "ok", 200

def log(mess):
    print(mess)
    sys.stdout.flush()

if __name__ == '__main__':
    app.run(debug = True)
