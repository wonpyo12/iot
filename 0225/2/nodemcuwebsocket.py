import sys
import werkzeug.serving



# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room
import json, time, os

app = Flask(__name__, template_folder=".")
socketio = SocketIO(app=app, logger=True, engineio_logger=True,cors_allowed_origins='*',async_mode='threading',allow_upgrades=True)
@socketio.on('message')
def handle_raw_message(data):
    print(f"받은 데이터: {data}")
    # 아두이노가 보낸 데이터가 문자열(JSON)이므로 웹 클라이언트로 그대로 중계@socketio.on('message')
def handle_raw_message(data):
    print(f"데이터 수신 성공: {data}")
    # NodeMCU에서 보낸 데이터가 JSON 문자열일 경우를 대비
    try:
        if isinstance(data, str):
            # 브라우저(WEB 룸)로 전달
            emit('dht_chart', {'data': data}, room='WEB', broadcast=True)
    except Exception as e:
        print(f"전달 오류: {e}")

# 2. 연결 시 로그 확인
@socketio.on('connect')
def handle_connect():
    print("어떤 클라이언트가 연결되었습니다!")
    emit('dht_chart', {'data': data}, room='WEB', broadcast=True)
@socketio.on('join_web')
def join_web(message):
    print('on_join_web')
    join_room('WEB')

@socketio.on('join_dev')
def join_dev(message):
    print('on_join_dev')
    join_room('DEV')

@socketio.on('led')
def controlled(message):
    l = message['data']
    if l == "ON":
        emit('led_control', {'data': 'on'}, room='DEV')
    elif l == "OFF":
        emit('led_control', {'data': 'off'}, room='DEV')

@socketio.on('events')
def getevents(message):
    emit('dht_chart', {'data': message}, room='WEB')

@socketio.on_error()
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))

@app.route('/dhtchart')
def dht22chart():
    return render_template("dhtchart.html")

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True, use_reloader=False)