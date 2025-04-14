from flask import Flask, request, jsonify
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/trend', methods=['GET'])
def trend():
    term = request.args.get('term')
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([term], cat=0, timeframe='now 7-d', geo='US')
    data = pytrends.interest_over_time().reset_index().to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run()
