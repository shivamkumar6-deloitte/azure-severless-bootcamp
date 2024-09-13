import logging
import json
import time
import random
import azure.functions as func
from azure.eventhub import EventHubProducerClient, EventData

def generate_telemetry(device_id):
    return {
        "device_id": device_id,
        "timestamp": time.time(),
        "aqi": random.randint(0, 500),
        "temperature": random.uniform(10, 40),
        "humidity": random.uniform(20, 80),
        "co2": random.uniform(300, 2000)
    }

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="iotair/{device_id?}", methods=["GET"])
def http_trigger_iot_air2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP trigger received a request to send data to Event Hub.')
    device_id = req.route_params.get('device_id','AQ_sensor_001')
    telemetry_data = generate_telemetry(device_id)
    

    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name)
    event_data = EventData(json.dumps(telemetry_data))

    with producer:
        producer.send_batch([event_data])
        
    return func.HttpResponse(f"Data sent to Event Hub: {telemetry_data}", status_code=200)


@app.service_bus_queue_trigger(arg_name="azservicebus", queue_name="iotairdata",
                               connection="smartcityservicebus_SERVICEBUS") 
def servicebus_trigger(azservicebus: func.ServiceBusMessage):
    logging.info('Python ServiceBus Queue trigger processed a message: %s',
                azservicebus.get_body().decode('utf-8'))
