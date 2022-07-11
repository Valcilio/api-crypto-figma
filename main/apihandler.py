import os
from flask import Flask, request, Response
from ..domain.gateways.mainapi import MainAPI

app = Flask(__name__)

@app.post('/framework_data')
def crypto_forecast():
    '''Get json with instructions for get data, run pipeline and 
    reponse with json containing all data'''

    framework_json = request.get_json()

    if framework_json: 
        if isinstance(framework_json, dict): 
            pass

        pipeline = MainAPI(framework_json=framework_json)
        df_response = pipeline.run()

        return df_response.to_json(orient='records', date_format='iso')
    else:
        return Response('{}', status='200', mimetype='application/json')

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)
