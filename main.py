import asyncio
import websockets
from flask import Flask, request, send_file
import threading
from getEnvironmentData import GetEnvironmentData
from saveDayliData import SaveData
import json

app = Flask(__name__)

# Definir la función de servidor WebSocket
async def websocket_server(websocket, path):
    try:
        while True:
            message = GetEnvironmentData()
            await websocket.send(message)
            await asyncio.sleep(1)  # Esperar un segundo antes de enviar el próximo mensaje
    except websockets.exceptions.ConnectionClosedOK:
        print("Conexión cerrada por el cliente")

# Configurar el servidor WebSocket
start_websocket_server = websockets.serve(websocket_server, "192.168.1.91", 8765)

# Definir las rutas HTTP
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_file(f"./dayliData/{filename}.csv", as_attachment=True)
    except FileNotFoundError:
        return 'Archivo no encontrado'

# Función para ejecutar el servidor Flask
def run_flask():
    app.run(host='192.168.1.91', port=80)

# Función asíncrona para guardar datos periódicamente
async def periodic_save_data():
    while True:
        data = GetEnvironmentData()
        data_dict = json.loads(data)
        humidity = data_dict["hum"]
        temperature = data_dict["temp"]
        sustrate_humidity = data_dict["sustrate_humidity"]
        SaveData(humidity=humidity,soilHumidity=sustrate_humidity,temperature=temperature)
        await asyncio.sleep(100)  # Esperar 300 segundos (5 minutos) antes de guardar nuevamente

# Ejecutar el bucle de eventos y ambos servidores en él
if __name__ == '__main__':
    # Iniciar el servidor Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Crear un bucle de eventos
    loop = asyncio.get_event_loop()

    # Ejecutar el servidor WebSocket en el bucle de eventos
    asyncio.ensure_future(start_websocket_server)

    # Ejecutar la tarea de guardado periódico en el bucle de eventos
    asyncio.ensure_future(periodic_save_data())

    # Iniciar el bucle de eventos
    loop.run_forever()
