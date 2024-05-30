# flask --app main --debug run
from flask import Flask,send_file,request
from flask_socketio import SocketIO,send
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
    ##currentData= GetEnvironmentData() 
    while True:
        currentData= GetEnvironmentData()
        await asyncio.sleep(2)
        return currentData







if __name__ == '__main__':
     SocketIO.run(app=app)