from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_super_chat_key'
# รองรับการทำงานแบบ Real-time
socketio = SocketIO(app, cors_allowed_origins="*")

# กำหนด Timezone เป็นประเทศไทย
TZ_BANGKOK = pytz.timezone('Asia/Bangkok')

@app.route('/')
def index():
    # หน้าแรกของเว็บ
    return render_template('index.html')

@socketio.on('send_message')
def handle_message(data):
    # รับข้อความจากผู้ใช้ -> ใส่เวลาไทย -> ส่งต่อให้ทุกคนในเว็บทันที
    now = datetime.now(TZ_BANGKOK)
    current_time = now.strftime("%H:%M") # รูปแบบ เวลา:นาที เช่น 16:45
    
    chat_data = {
        'username': data['username'],
        'message': data['message'],
        'time': current_time
    }
    
    # broadcast=True คือส่งให้ทุกคนที่เปิดหน้าเว็บนี้อยู่เห็นพร้อมกัน
    emit('receive_message', chat_data, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)