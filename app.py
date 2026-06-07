from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz
import os  # ดึงระบบ OS มาช่วยหา Port ของ Render

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_super_chat_key'

# อัปเกรดระบบดักจับข้อความแบบสากลให้เซิร์ฟเวอร์ออนไลน์รองรับ
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

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
    # เปลี่ยนให้ดึง Port ที่ Render จัดสรรมาให้โดยอัตโนมัติ เพื่อไม่ให้ชนกัน
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
