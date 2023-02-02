import requests, json
import time
import asyncio

#Librerias de Influxbd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

async def datos(): 
    # esta es la URL completa con la informacion concatenada para realizar la petición correcta
    complete_url = "https://api.openweathermap.org/data/2.5/weather?q=Cali&appid=d5f83c4afd675ba05b9c4c4d6aac065f&units=metric"
    # Ejecutamos la consulta
    response = requests.get(complete_url)
    # Obtenemos la respuesta en formato JSON
    x = response.json()
    if x["cod"] == 200:
        # En “main” se encuentra la informacion principal del estado del tiempo
                
        current_temperature = x["main"]["temp"] # Almacenamos la temperatura        
        current_pressure = x["main"]["pressure"] # presion atmosferica
        current_humidity = x["main"]["humidity"]  # humedad
        
        
             
        return current_temperature ,current_pressure,current_humidity

    
if __name__ == "__main__":
    bucket = 'bucket'
    token_influx = 'k9_G4H6JMyl33AFu9FOXgdwsCVBDFlkXzkoYH72qM1GR70RHcgwJcxMfivBY2oUX1LV1ee_DOzjWyQG8AS4TUA=='
    client = InfluxDBClient(url="http://172.29.0.2:8086", token=token_influx, org="org")
    write_api = client.write_api(write_options=SYNCHRONOUS)
    query_api = client.query_api()
    while(True):
        temp,pres,hum = asyncio.run(datos())
        p = Point("my_measurement").tag("location", "Cali").field("temperature", temp)
        write_api.write(bucket=bucket, record=p)
        p1 = Point("my_measurement").tag("location", "Cali").field("pressure", pres)
        write_api.write(bucket=bucket, record=p1)
        p2 = Point("my_measurement").tag("location", "Cali").field("humidity", hum)
        write_api.write(bucket=bucket, record=p2)
        print(f'Temperatura: {temp} \nPresion atmosferica: {pres} \nHumedad: {hum}')
        time.sleep(20)
