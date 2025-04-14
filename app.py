from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/trend', methods=['GET'])
def trend():
    term = request.args.get('term')
    if not term:
        return jsonify({'error': 'No term provided'}), 400

    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([term], cat=0, timeframe='now 7-d', geo='US')
    data = pytrends.interest_over_time()

    if data.empty:
        return jsonify({'error': 'No data found for the term'}), 404

    data.reset_index(inplace=True)
    data = data[['date', term]]
    data.rename(columns={term: 'value'}, inplace=True)
    return jsonify(data.to_dict(orient='records'))
