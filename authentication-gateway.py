from flask import Flask
from flask import request, redirect
from flask.helpers import url_for
from flask.templating import render_template
import requests
from flask.wrappers import Response

app = Flask(__name__)

AUTH_API = "https://safewalk-integration.no-ip.org:8443/api/v1/auth/authenticate/"
OAUTH_TOKEN = "bd5c8c657490a84382cb5a622066d3cdef21a3c8"

def login_action(username, password, destination=""):
    payload = {
        'username' : username,
        'password' : password,
    }
    headers = {'AUTHORIZATION': 'Bearer {}'.format(OAUTH_TOKEN)}
    r = requests.post(AUTH_API, data=payload, headers=headers, verify=False)
    if r.status_code==200:
        return redirect(destination or '/')
    elif r.status_code==401:
        json_res=r.json()
        code = json_res.get('code')
        if code=='ACCESS_CHALLENGE':
            return render_template('index.html', reply=json_res.get('reply-message'), username=username, destination=destination)
    return render_template('index.html', reply=json_res.get('reply-message'))


@app.route('/login', methods=['get', 'post'])
def index():
    if request.method == 'POST':
        return login_action(
            request.form['username'],
            request.form['password'],
            request.form['destination']
        )

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
