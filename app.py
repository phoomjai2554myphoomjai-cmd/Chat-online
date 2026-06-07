from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_super_chat_key'

socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

TZ_BANGKOK = pytz.timezone('Asia/Bangkok')

# 📝 กล่องความจำชั่วคราวสำหรับเก็บประวัติแชท (จำได้สูงสุด 50 ข้อความล่าสุด)
CHAT_HISTORY = []
HISTORY_LIMIT = 50

@app.route('/')
def index():
    return render_template('index.html')

# 🤝 ดักจับตอนที่มีคนเปิดหน้าเว็บหรือกดเข้าห้องแชทสำเร็จ
@socketio.on('connect')
def handle_connect():
    # ส่งข้อความเก่าทั้งหมดที่มีอยู่ในกล่องความจำ ไปให้คนที่เพิ่งเข้ามาคนนี้คนเดียวเห็น
    emit('load_history', CHAT_HISTORY)

@socketio.on('send_message')
def handle_message(data):
    now = datetime.now(TZ_BANGKOK)
    current_time = now.strftime("%H:%M")
    
    chat_data = {
        'username': data['username'],
        'message': data['message'],
        'time': current_time
    }
    
    # 💾 จดบันทึกข้อความนี้ลงในกล่องความจำ
    CHAT_HISTORY.append(chat_data)
    
    # ถ้าข้อความเยอะเกินไป ให้ลบข้อความเก่าสุดออกเพื่อประหยัดแรมเซิร์ฟเวอร์
    if len(CHAT_HISTORY) > HISTORY_LIMIT:
        CHAT_HISTORY.pop(0)
        
    emit('receive_message', chat_data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
