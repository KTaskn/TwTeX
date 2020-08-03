# coding:utf-8
import os
import json
import base64
from PIL import Image
from io import BytesIO
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

def call_tweet(key, secret, tweet, img_binary):
    auth = tweepy.OAuthHandler(os.environ['CK'], os.environ['CS'])
    auth.set_access_token(key, secret)
    api = tweepy.API(auth)
    media_ids = []
    media_ids.append(
        api.media_upload(filename='twtex.png', file=BytesIO(img_binary)).media_id_string
    )
    api.update_status(status=tweet, media_ids=media_ids)

    return

@app.route("/tweet", methods=["POST"])
@cross_origin("*")
def tweet():
    if request.method in ['OPTIONS']:
        return

    if request.data:
        data = json.loads(request.data.decode('utf-8'))
    else:
        return jsonify({"result": "NG"})

    if ('tweet' in data
        and data['tweet']
        and 'img_b64' in data
        and data['img_b64']):

        text_tweet = data['tweet']
        img_b64 = data['img_b64']
        img_b64 += "=" * ((4 - len(img_b64) % 4) % 4)
        # 環境依存の様(","で区切って本体をdecode)
        img_binary = base64.b64decode(img_b64.split(',')[1])

        if ('access_token' in data
            and data['access_token']
            and 'access_token_secret' in data
            and data['access_token_secret']):

            key = data['access_token']
            secret = data['access_token_secret']
            call_tweet(key, secret, text_tweet, img_binary)

            return jsonify({
                "result": "OK",
                "access_token": key,
                "access_token_secret": secret
            })

        elif ('oauth_token' in data
            and data['oauth_token']
            and 'oauth_verifier' in data
            and data['oauth_verifier']):

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
            call_tweet(key, secret, text_tweet, img_binary)

            return jsonify({
                "result": "OK",
                "access_token": key,
                "access_token_secret": secret
            })
        else:
            pass
    else:
        pass

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