# flask --app main --debug run
from flask import Flask,send_file,request
from flask_socketio import SocketIO,emit
from getEnvironmentData import GetEnvironmentData
import asyncio 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio  =SocketIO(app)


@app.route('/sendFiles',methods=['GET'])
def index():
    fileName  = request.args.get('filename')
    print(fileName)
    return send_file(f"./dayliData/{fileName}",as_attachment=True)



@socketio.on('sendCurrentData')
async def handleMessage(msg):
    client_id = request.sid
    while True:
        currentData = GetEnvironmentData()
        # Envía los datos al cliente utilizando el identificador único
        emit('currentData', currentData, room=client_id)  
        await asyncio.sleep(2)






if __name__ == '__main__':
     SocketIO.run(app=app)