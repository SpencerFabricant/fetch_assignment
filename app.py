from flask import Flask
from flask import request
from flask import Response
import uuid
import json
import math

app = Flask(__name__)



def score_receipt(receipt):
    score = 0
    print(receipt)
    for i in receipt['retailer']:
        if i.isalpha():
            score += 1
    print(score)

    cents = int(receipt['total'].split('.')[1])
    if cents == 0:
        score += 50

    if cents %25 == 0:
        score += 25
    print(score)

    score += 5 * (len(receipt['items'])//2)
    print(score)

    for item in receipt['items']:
        if len(item['shortDescription'].strip()) % 3 == 0:
            score += int(math.ceil(float(item['price']) * 0.2))
    print(score)

    if int(receipt['purchaseDate'].split('-')[2]) % 2 == 1:
        score += 6
    print(score)

    purchase_hour = int(receipt['purchaseTime'].split(':')[0])
    if purchase_hour in [14, 15]:
        score += 10
    print(score)

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
        return Response("no", status=400)
    return Response(receipt_id, status=200)

@app.route('/receipts')
@app.route('/receipts/<receipt_id>/points')
def uuid_to_score(receipt_id):
    print(receipt_id)
    return f"{receipts[receipt_id]}"


