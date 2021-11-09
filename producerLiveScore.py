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
  "apikey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"}

paramsAPI = (
   ("season_id","xxx"),
   ("date_from","2021-09-19"),
   ("live","true")
)

def create_message(jsondata):
    jsonRes = []
    for game in jsondata["data"]:
        minute = game["minute"]
        home = game["home_team"]["name"]
        away = game["away_team"]["name"]
        hscore = game["stats"]["home_score"]
        ascore = game["stats"]["away_score"]
        #print(home, hscore, " - ", ascore, away)
        jsonTupla = {"home": home, "hscore": hscore, "away": away, "ascore": ascore, "minute": minute}
        jsonRes.append(jsonTupla)
    return json.dumps(jsonRes)

while True:
    time.sleep(30)
    response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=paramsAPI)
    print(response.text)
    
    jsondata = json.loads(response.text)
    if not jsondata["data"]:
        print("SONO DENTRO")
        message = "null"
        channel.basic_publish(exchange='livescore', routing_key='livescore_queue', body=message)
        break
    message = create_message(jsondata)
    print("\nSTAMPA MESSAGGIO\n", message)
    channel.basic_publish(exchange='livescore', routing_key='livescore_queue', body=message)

connection.close()

print("Exit from function!!!!")