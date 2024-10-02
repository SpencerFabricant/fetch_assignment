from flask import Flask
from flask import request
from flask import Response
import uuid
import json
import math

app = Flask(__name__)



def score_receipt(receipt):
    score = 0
    for i in receipt['retailer']:
        if i.isalpha():
            score += 1

    cents = int(receipt['total'].split('.')[1])
    if cents == 0:
        score += 50

    if cents %25 == 0:
        score += 25

    score += 5 * (len(receipt['items'])//2)

    for item in receipt['items']:
        if len(item['shortDescription'].strip()) % 3 == 0:
            score += int(math.ceil(float(item['price']) * 0.2))

    if int(receipt['purchaseDate'].split('-')[2]) % 2 == 1:
        score += 6

    purchase_hour = int(receipt['purchaseTime'].split(':')[0])
    if purchase_hour in [14, 15]:
        score += 10

    return score


receipts = {}


@app.route('/receipts/process', methods=["POST"])
def process_receipt():
    data = json.loads(request.data)
    try:
        points = score_receipt(data)
        receipt_id = str(uuid.uuid4())
        receipts[receipt_id] = points
    except:
        return Response("Receipt is Invalid", status=400)

    return_json = json.dumps({"id": receipt_id})
    return Response(return_json, status=200)

@app.route('/receipts')
@app.route('/receipts/<receipt_id>/points')
def uuid_to_score(receipt_id):
    if receipt_id not in receipts:
        return Response("Invalid receipt id", status=404)
    return_json = json.dumps({"score":receipts[receipt_id]})
    return Response(return_json, status=200)


