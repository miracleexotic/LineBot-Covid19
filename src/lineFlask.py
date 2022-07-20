from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage
)
from linebot.models import *

from flask import Flask, request, abort
from datetime import datetime
import json

from dataHandle import Data
from messageFlexData import myFlexDate, myFlexCovid


app = Flask(__name__)

with open('../authentication/config.json') as fh:
    config = json.load(fh)

line_bot_api = LineBotApi(config['line']['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(config['line']['CHANNEL_SECRET'])

@app.route("/home")
def index():
    """Use for testing that API is running."""
    return "API for Line OA Covid-19"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    """Handle location event."""
    profile = line_bot_api.get_profile(event.source.user_id)

    position = []
    position.append(str(profile.display_name)) # 0
    dateTime = datetime.fromtimestamp((int(event.timestamp) // 1000) + 25200).strftime("%d/%m/%Y, %H:%M:%S").split(", ")
    position.append(dateTime[0]) # 1
    position.append(dateTime[1]) # 2
    position.append(str("")) # 3
    position.append(str(event.message.title)) # 4
    position.append(str(event.message.address)) # 5
    position.append(f"({event.message.latitude}, {event.message.longitude})") # 6
    print(position)

    myData = Data(profile.user_id)
    myData.insertData_inside(position)
    myData.delRow()

    data = str(event.message.title) + "\n" + str(event.message.address) + "\n" + position[1] + ", " + position[2]
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=str(data)))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle message event."""
    profile = line_bot_api.get_profile(event.source.user_id)

    if event.message.text == 'เข้า':
        text_message = TextSendMessage(text='ที่ไหน?',quick_reply=QuickReply(items=[QuickReplyButton(action=LocationAction(label="ค้นหาสถานที่"))]))
        line_bot_api.reply_message(
            event.reply_token,
            text_message)

    if event.message.text == 'ออก':
        dateTime = datetime.fromtimestamp((int(event.timestamp) // 1000) + 25200).strftime("%H:%M:%S")
        myData = Data(profile.user_id)
        myData.insertData_outside(dateTime)
    
    if event.message.text == 'Timeline':
        data = myFlexDate(profile.user_id)
        flex_message = data.createFlex()
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)

    if event.message.text == 'Covid19':
        data = myFlexCovid()
        flex_message = data.createFlex()
        line_bot_api.reply_message(
            event.reply_token,
            flex_message)
    
    if event.message.text == 'id':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=str(profile.user_id)))


if __name__ == "__main__":
    app.run(debug=True)
