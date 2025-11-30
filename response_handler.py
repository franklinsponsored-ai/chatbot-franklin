import uuid
from flask import Flask, request, make_response, jsonify
import requests
import json
import rp_json
import constants as ct

app = Flask(__name__)

def get_rasa_response(message):
    """ Send input text to Rasa NLU and return parsed intent & entities """

    rasa_url = f"http://{ct.RASA_HOST}:5005/model/parse"

    payload = {"text": message}

    try:
        response = requests.post(rasa_url, json=payload)
        rasa_data = response.json()

        return rasa_data

    except Exception as e:
        print(f"Error contacting Rasa: {e}")
        return {
            "intent": {"name": "none", "confidence": 0.0},
            "entities": [],
            "text": message
        }


@app.route('/', methods=['GET'])
def handle_unknown_response():
    """ Receives unexpected RapidPro user input and returns Rasa NLU response """

    unexpected_input = request.args.get('unknown_response')

    if unexpected_input is None or unexpected_input.strip() == "":
        print("User input is empty")
        return "user input is empty"

    print("User input: " + unexpected_input)

    # ---- Call Rasa instead of Dialogflow ----
    rasa_response = get_rasa_response(unexpected_input)
    print("Rasa response:", rasa_response)

    # Build RapidPro-friendly object
    intent_name = rasa_response["intent"]["name"]
    fulfillment_text = ""   # Rasa NLU doesn't generate text; only classification
    parameters = {}

    # Extract entities
    if "entities" in rasa_response:
        for ent in rasa_response["entities"]:
            parameters[ent["entity"]] = ent["value"]

    # If your rp_json class requires full DF-like structure, simulate it:
    df_like_response = {
        "intent": {"display_name": intent_name},
        "parameters": parameters,
        "query_text": unexpected_input,
        "fulfillment_text": fulfillment_text
    }

    rp_response = rp_json.RP_JSON(df_like_response)
    print("RP Response:", rp_response)

    return make_response(
        jsonify({
            'intent': rp_response.intent,
            'fulfillment': rp_response.fulfillment_text,
            'parameters': rp_response.parameters,
            'user_query': rp_response.query_text
        })
    )


if __name__ == "__main__":
    app.run(debug=True, port=8080)
