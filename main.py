# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os

import dialogflow as dialogflow
import requests
from flask import render_template, Flask, jsonify, request

app = Flask(__name__)
GOOGLE_APPLICATION_CREDENTIALS=os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', "config/codebot-xnpp-bdcf7960398a.json")

@app.route('/codebot', methods=['POST'])
def codebot(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    message = request.GET.get('message')
    projectid = 'codebot-xnpp'
    response_received = detect_intent_texts(project_id=projectid, text=message,
                                            language_code='en')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_message', methods=['POST'])
def send_message():
    #message = request.args.get('message')
    message = request.form['message']
    print("Input message: ", message)
    #project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    project_id = 'codebot-xnpp'
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    print("Fulfillment text: ", fulfillment_text)
    response_text = { "message":  fulfillment_text }
    return jsonify(response_text)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    print("Webhook data: ", data)
    if data['queryResult']['queryText'] == 'yes':
        reply = {
            "fulfillmentText": "This is the information I have found: ",
        }
        return jsonify(reply)

    elif data['queryResult']['queryText'] == 'no':
        reply = {
            "fulfillmentText": "Glad to help. See you soon.",
        }
        return jsonify(reply)


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        print("Text input: ", text_input)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        print("Response: ", response)
        return response.query_result.fulfillment_text


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=False)
