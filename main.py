import asyncio
import websockets
from flask import Flask, request, send_file
from getEnvironmentData import GetEnvironmentData
from saveDayliData import SaveData

app = Flask(__name__)

# Definir la función de servidor WebSocket
async def websocket_server(websocket, path):
    try:
        while True:
            message = GetEnvironmentData()
            await websocket.send(message)
    except websockets.exceptions.ConnectionClosedOK:
        print("Conexión cerrada por el cliente")

# Configurar el servidor WebSocket
start_websocket_server = websockets.serve(websocket_server, "localhost", 8765)

# Definir las rutas HTTP

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(f"./dayliData/{filename}.csv", as_attachment=True)
    except FileNotFoundError:
        return 'Archivo no encontrado'

# Ejecutar ambos servidores en un bucle de eventos
if __name__ == '__main__':
    # Iniciar el servidor WebSocket
    asyncio.get_event_loop().run_until_complete(start_websocket_server)
    asyncio.get_event_loop().run_forever()

    # Iniciar el servidor Flask
    app.run(host='192.168.1.91', port=80)

while True:
    SaveData()
    asyncio.sleep(300)