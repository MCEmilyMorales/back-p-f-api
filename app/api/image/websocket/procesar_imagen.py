from app.api.image.websocket.s3_client import s3_client, BUCKET_NAME
import requests
from app.api.image import calculos, route
import json
from io import BytesIO

CONDASERVER_URL = "http://localhost:9000/procesar_imagen/"

def run_async_procesar(file_location: str, imagen_id: str, file: bytes, informe_id: str):

    print(" 📱 Llamando a run_async_procesar")
    import asyncio
    asyncio.run(procesar_imagen(file_location, imagen_id, file, informe_id))

async def procesar_imagen(file_location: str, imagen_id: str, file: bytes, informe_id: str):
    try:
        
        print("🔜 Iniciando procesamiento de imagen")
        print(f" 🤞 Imagen ID: {file_location}")

        # Subir al S3
        print(f"🔼 {file_location}")
        file_stream = BytesIO(file) # Resetear el puntero del archivo antes de subir
        s3_client.upload_fileobj(file_stream, BUCKET_NAME, file_location)

        # Llamada al servidor de análisis
        
        print(f"💌 Enviando solicitud POST a {CONDASERVER_URL} con ubicación: {file_location}")
        response = requests.post(CONDASERVER_URL, json={"ubicacion": file_location})
        print(f" 🔊 Respuesta del servidor: código {response.status_code}")
        if response.status_code != 200:
            print("🙇 Error en la comunicación con el servidor de procesamiento")
            return {"error": "Error en la comunicación con el servidor de procesamiento."}

        json_data = response.json()
        print("🚨 Respuesta JSON recibida del servidor de análisis")

        # Procesar resultado
        resultado = calculos.PorcentajePositivos(json_data)
        print(f" 〽 Resultado procesado: {resultado}")

        # Guardar resultado en S3
        json_key = f"procesados/{file_location}.json"
        print(f"🧗‍♀️ Subiendo resultado procesado a S3 con clave: {json_key}")
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=json_key,
            Body=json.dumps(json_data),
            ContentType="application/json"
        )

        # Enviar resultado al WebSocket si está conectado
        if imagen_id in route.active_connections:
            print(f"📫 Enviando resultado al WebSocket para imagen_id: {imagen_id}")
            await route.active_connections[imagen_id].send_json(resultado)
        else:
            print(f"🚩 No hay conexión WebSocket activa para imagen_id: {imagen_id}")
            
    except Exception as e:
        print(f"🏳 Ocurrió una excepción: {e}")
        if imagen_id in route.active_connections:
            await route.active_connections[imagen_id].send_text(f"Error: {str(e)}")
