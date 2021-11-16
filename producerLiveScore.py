import pika 
import time 
import requests
import json

print("Collegamento a RabbitMQ...")

params = pika.ConnectionParameters(host="localhost")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue = 'livescore_queue')

channel.exchange_declare(exchange='livescore', exchange_type='direct')

print("...eseguito")

headers = { 
  "apikey": "50db53c0-25f4-11ec-911e-cf7d4f57f34d"}

paramsAPI = (
   ("season_id","392"),
   ("date_from","2021-09-19"),
   ("live","true")
)

def create_message(jsondata):
    jsonRes = []
    if not jsondata["data"]:
        return json.dumps(None)
    else:
        for game in jsondata["data"]:
            minute = game["minute"]
            home = game["home_team"]["name"]
            away = game["away_team"]["name"]
            hscore = game["stats"]["home_score"]
            ascore = game["stats"]["away_score"]
            jsonTupla = {"home": home, "hscore": hscore, "away": away, "ascore": ascore, "minute": minute}
            jsonRes.append(jsonTupla)
    return json.dumps(jsonRes)

while True:
    time.sleep(30)
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=paramsAPI)
    print(response.text)
    
    jsondata = json.loads(response.text)
    message = create_message(jsondata)
    if json.loads(message) is None: 
        break
    channel.basic_publish(exchange='livescore', routing_key='livescore_queue', body=message)

connection.close()

print("Exit from function.")


