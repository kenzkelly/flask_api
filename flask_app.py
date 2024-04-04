from flask import Flask, request, jsonify 
from predictor import Predictor 
import json
import spacy   

app = Flask(__name__)

@app.route('/json', methods = ['POST'])
def hello_world():
    data = json.loads(request.get_json())

    o = data.get('Openness')
    c = data.get("Conscientious")
    e = data.get("Extraversion")
    a = data.get("Agreeable")
    n = data.get("Neuroticism")

    predictor = Predictor(o, c, e, a, n)
    predictions = predictor.compute_similarity("job_traits2.csv")

    return predictions