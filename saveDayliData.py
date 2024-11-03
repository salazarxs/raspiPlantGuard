import pandas as pd
import os
from datetime import datetime

def SaveData(humidity, soilHumidity, temperature):

    # Crear el directorio si no existe
    os.makedirs('./dayliData', exist_ok=True)

    # Obtener la fecha actual
    today = datetime.now()
    fecha_str = today.strftime('%Y-%m-%d')

    # Formatear el nombre del archivo con la fecha
    archivo_csv = f'./dayliData/{fecha_str}_plantGuard.csv'

    try:
        # Verificar si el archivo está vacío (primera vez guardando datos)
        file_exists = os.path.isfile(archivo_csv) and os.stat(archivo_csv).st_size > 0
        if(soilHumidity):
            # Crear el nuevo registro como diccionario
            nuevo_registro = {
            "date": [fecha_str],
            "humidity": [humidity],
            "soilHumidity": [soilHumidity],
            "temperature": [temperature]
            }
        else:
            nuevo_registro = {
            "date": [today],
            "humidity": [humidity],
            "soilHumidity": [soilHumidity],
            "temperature": [0]
            }
        # Convertir a DataFrame
        df_nuevo_registro = pd.DataFrame(nuevo_registro)

        # Guardar el DataFrame en el archivo, incluyendo el encabezado solo si el archivo está vacío
        df_nuevo_registro.to_csv(archivo_csv, mode='a', index=False, header=not file_exists)
        print(f'Data saved successful on {fecha_str}')
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False
