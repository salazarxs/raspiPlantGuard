import pandas as pd
import os
from datetime import datetime

def SaveData(humidity, soilHumidity, temperature):

    # Crear el directorio si no existe
    os.makedirs('./dayliData', exist_ok=True)

    # Obtener la fecha actual
    today = datetime.now()
    fecha_str = today.strftime('%Y-%m-%d %H:%M')  # Incluye horas y minutos

    # Formatear el nombre del archivo con la fecha
    archivo_csv = f'./dayliData/{today.strftime("%Y-%m-%d")}_plantGuard.csv'  # Usamos solo la fecha para el nombre del archivo

    try:
        # Verificar si el archivo está vacío (primera vez guardando datos)
        file_exists = os.path.isfile(archivo_csv) and os.stat(archivo_csv).st_size > 0
        if soilHumidity is not None:  # Verificar si soilHumidity es diferente de None
            # Crear el nuevo registro como diccionario
            nuevo_registro = {
                "date": [fecha_str],  # Cambiamos a incluir horas y minutos
                "humidity": [humidity],
                "soilHumidity": [soilHumidity],
                "temperature": [temperature]
            }
        else:
            nuevo_registro = {
                "date": [fecha_str],  # Cambiamos a incluir horas y minutos
                "humidity": [humidity],
                "soilHumidity": [None],  # Cambia a None si no hay humedad del suelo
                "temperature": [0]
            }
        
        # Convertir a DataFrame
        df_nuevo_registro = pd.DataFrame(nuevo_registro)

        # Guardar el DataFrame en el archivo, incluyendo el encabezado solo si el archivo está vacío
        df_nuevo_registro.to_csv(archivo_csv, mode='a', index=False, header=not file_exists)
        print(f'Data saved successfully on {fecha_str}')  # Mensaje con fecha y hora
        return True
    except Exception as e:
        print(f"Error al guardar los datos: {e}")
        return False
