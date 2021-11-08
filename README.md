# SCIOT-LiveScore
| **Petrazzuolo Lorenzo** | **0522500894** |
| --- | --- | 

Exam project for _Serverless Computing for IoT_ of the course year 2020/2021. Master's degree in Computer Science. 
___

The idea of this project is to have a system of Livescore about Football matches. In detail, the system permits to check the results of Football matches in real time and, when one of them changes, a Telegram message is sent to the user with the updated result. In the message there are info about the minute of the gol event and the updated result. In addiction to this, a Telegram message is sent when the Football match is over. 

## Architecture

The architecture of the project is composed by several components. A Python script, deployed and run in local, sends every 30 seconds a request to an API of [__Sport Data API__](https://sportdataapi.com/) (livescore data provider). The received data contain the scores of Football matches in real time of a certain League (in our case "Serie A"). The data are organized in a JSON object and sent to a queue of the RabbitMQ message broker. Receiving the message on the queue triggers a serverless function deployed on Nuclio. The first time, the function saves the state of the scores, from the second time, the state is compared with the new scores. If the score is different, a message is sent to a Telegram user with information on live and minute result, if the match is over a message with the names of Football teams and the final result is sent, if all the Football matches are over, a notification message is sent to the Telegram user and both Nuclio function and local function are stopped. 

![architecture](./media/architecture.png)

## Prerequisites

- Docker and Docker Compose (Application containers engine)
- Nuclio (Serverless computing provider)
- RabbitMQ (AMQP and MQTT message broker)
- Python (version >3.7)

## Installation



