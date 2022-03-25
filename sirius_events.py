import base64
import requests

def get_user(email, password):
    token = base64.b64encode(f'{email}:{password}'.encode()).decode()

    headers = {
        'Authorization': 'Basic ' + token
    }

    params = {
        'fid': '199910000004',
        '__act': 'send',
        '__api': '2'
    }

    response = requests.get('https://online.sochisirius.ru/forms', params=params, headers=headers)
    data = response.json()

    if not data.get('status') or data['status'].get('v') != '1':
        raise Exception('authorization failed: ' + str(data))

    return {
        'user_id': data['f_id']['v'],
        'token': token
    }

def enroll_event(event_id, user_id, token):
    headers = {'Authorization': 'Basic ' + token}

    data = {
        'id': event_id,
        'fid': '199910202940',
        'act': 'send',
        '__api': '2',
        'f_1032910003': user_id,
        'task': 'edit'
    }

    response = requests.post('https://online.sochisirius.ru/forms', data=data, headers=headers)
    data = response.json()

    if data.get('enrolled') and data['enrolled'].get('e') is not None:
        return f"error response: {data['enrolled']['e']}"

    if response.status_code != 200:
        return f'bad status code {response.status_code}: {response.text}'

    return 'success'
