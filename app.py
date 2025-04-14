from flask import Flask, request, jsonify
from pytrends.request import TrendReq
import pandas as pd

app = Flask(__name__)

@app.route('/trend', methods=['GET'])
def trend():
    try:
        term = request.args.get('term')
        if not term:
            return jsonify({'error': 'Missing "term" parameter'}), 400

        pytrends = TrendReq(
            hl='en-US',
            tz=360,
            timeout=(10, 25),
            retries=2,
            backoff_factor=0.1,
            requests_args={'headers': {'User-Agent': 'Mozilla/5.0'}}
        )

        pytrends.build_payload([term], cat=0, timeframe='now 7-d', geo='US')
        data = pytrends.interest_over_time()

        if data.empty:
            return jsonify({'error': f'No trend data found for term: {term}'}), 404

        data.reset_index(inplace=True)
        result = data[['date', term]].to_dict(orient='records')
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
