import asyncio
import websockets
from flask import Flask, request, send_file

app = Flask(__name__)

# Definir la función de servidor WebSocket
async def websocket_server(websocket, path):
    try:
        while True:
            message = await websocket.recv()
            print(f"Mensaje recibido: {message}")
            await websocket.send("Mensaje recibido por el servidor")
    except websockets.exceptions.ConnectionClosedOK:
        print("Conexión cerrada por el cliente")

# Configurar el servidor WebSocket
start_websocket_server = websockets.serve(websocket_server, "localhost", 8765)

# Definir las rutas HTTP
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
        return 'Archivo guardado correctamente'
    else:
        return 'No se ha enviado ningún archivo'

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return 'Archivo no encontrado'

# Ejecutar ambos servidores en un bucle de eventos
if __name__ == '__main__':
    # Iniciar el servidor WebSocket
    asyncio.get_event_loop().run_until_complete(start_websocket_server)
    asyncio.get_event_loop().run_forever()

    # Iniciar el servidor Flask
    app.run(host='0.0.0.0', port=80)
