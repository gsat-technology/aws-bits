import json
import requests
from requests.auth import HTTPBasicAuth


def handler(event, context):

    auth = HTTPBasicAuth(event['user'], event['api-key'])
    headers = {'Plotly-Client-Platform': 'python'}


    headers = {
                'Content-Type': 'application/json',
                'Plotly-Client-Platform': 'curl'
            }


    r = requests.post(
            'https://api.plot.ly/v2/grids/{}:{}/row'.format(event['user'], event['grid']),
            auth=auth,
            headers=headers,
            json={'rows': event['rows']}
        )

    print(r.status_code)
    print(r.text)

    if str(r.status_code)[0] == '2':
        return {'status': 'okay'}
    else:
        return {'status': 'error', 'reason': r.text}
