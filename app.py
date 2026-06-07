from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_super_chat_key'

# ปรับให้ยืดหยุ่นที่สุดสำหรับรันบนคลาวด์ฟรี
socketio = SocketIO(app, cors_allowed_origins="*")

TZ_BANGKOK = pytz.timezone('Asia/Bangkok')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    now = datetime.now(TZ_BANGKOK)
    current_time = now.strftime("%H:%M")
    
    chat_data = {
        'username': data['username'],
        'message': data['message'],
        'time': current_time
    }
    emit('receive_message', chat_data, broadcast=True)

if __name__ == '__main__':
    # ดึง Port จาก Render มาใช้ และเปิดรับสัญญาณรอบทิศทาง (0.0.0.0)
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
