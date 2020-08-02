# coding:utf-8
import os
import json
from urllib.parse import parse_qsl
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS, cross_origin
import tweepy

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.environ['SESSION_SECRET']

@app.route("/")
def main():
    return """
    <html>
    <head></head>
    <body>
    <form action="/tweet" method="post">
        <input type="text" name="tweet" />
        <input type="submit" value="送信" />
    </form>
    </body>
    </html>
    """

@app.route("/tweet", methods=["POST"])
@cross_origin("*")
def tweet():
    if request.method in ['OPTIONS']:
        return

    if request.data:
        data = json.loads(request.data.decode('utf-8'))
    else:
        return jsonify({"result": "NG"})

    if ('oauth_token' in data
        and data['oauth_token']
        and 'oauth_verifier' in data
        and data['oauth_verifier']):
        text_tweet = data['tweet']

        auth = tweepy.OAuthHandler(os.environ['CK'], os.environ['CS'])

        token = data['oauth_token']
        verifier = data['oauth_verifier']

        auth.request_token = {
            'oauth_token' : token,
            'oauth_token_secret' : verifier
        }
        auth.get_access_token(verifier)

        key = auth.access_token
        secret = auth.access_token_secret

        auth = tweepy.OAuthHandler(os.environ['CK'], os.environ['CS'])
        auth.set_access_token(key, secret)
        api = tweepy.API(auth)
        api.update_status(text_tweet)
        return jsonify({"result": "OK"})
    else:
        return jsonify({"result": "NG"})

@app.route("/login")
@cross_origin("*")
def login():
    callback_url = "https://babmgkolonhlmggmploddodegjfbccil.chromiumapp.org"
    auth = tweepy.OAuthHandler(os.environ['CK'], os.environ['CS'], callback_url)
    redirect_url = auth.get_authorization_url()

    return jsonify({
        "redirect": redirect_url
    })

@app.route("/callback")
def callback():
    auth = tweepy.OAuthHandler(os.environ['CK'], os.environ['CS'])
    verifier = request.args.get('oauth_verifier')
    
    token = request.args.get('oauth_token')

    auth.request_token = {
        'oauth_token' : token,
        'oauth_token_secret' : verifier
    }
    auth.get_access_token(verifier)
    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('main'))