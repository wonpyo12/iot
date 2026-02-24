import serial

import time

import mysql.connector

import threading

from flask import Flask, render_template,request

app = Flask(__name__)

# ── MySQL 연결 ──────────────────────────────

def get_connection():

    return mysql.connector.connect(

        host="localhost",

        user="pi",

        password="1234",

        database="sensor_db"

    )

# ── Arduino 데이터 읽기 ─────────────────────


# ── 데이터 저장 ─────────────────────────────

def save_to_db(temperature, humidity):

    conn   = get_connection()

    cursor = conn.cursor()

    sql    = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"

    cursor.execute(sql, (temperature, humidity))

    conn.commit()

    cursor.close()

    conn.close()

# ── 데이터 조회 ─────────────────────────────

def get_records(limit=10):

    conn   = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(

        "SELECT * FROM sensor_data ORDER BY recorded_at DESC LIMIT %s",

        (limit,)

    )

    rows = cursor.fetchall()

    cursor.close()

    conn.close()

    return rows

# ── 라우트 ──────────────────────────────────

@app.route('/')

def index():

    records = get_records()

    return render_template("index.html", records=records)
@app.route('/collect')
def collect():
    
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')    
    if temperature is not None and humidity is not None:
        try:
            # 3. 가져온 값을 숫자로 바꿔서 DB에 저장
            save_to_db(float(temperature), float(humidity))
            print(f"저장 성공: 온도 {temperature}, 습도 {humidity}")
            return f"성공: 온도 {temperature}, 습도 {humidity}", 200
        except Exception as e:
            print(f"DB 저장 오류: {e}")
            return "DB 저장 오류", 500
            
    
    return "데이터를 읽을 수 없습니다. (파라미터 누락)", 400

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
