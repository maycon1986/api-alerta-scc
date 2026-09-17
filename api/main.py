import base64, json, os, requests, functions_framework
from dotenv import load_dotenv
from cloudevents.http import CloudEvent

load_dotenv()
 
@functions_framework.cloud_event
def receber_mensagem(cloud_event: CloudEvent) -> None:
    # A mensagem Pub/Sub, dentro do CloudEvent entregue pelo Eventarc,
    # vem em cloud_event.data["message"]["data"], codificada em Base64.
    pubsub_message_b64 = cloud_event.data["message"]["data"]
    pubsub_message = base64.b64decode(pubsub_message_b64).decode("utf-8")
 
    # Converte a mensagem de string para um objeto JSON.
    message_data = json.loads(pubsub_message)
 
    # Capturando informações do bloco "finding" do JSON do SCC.
    severity = message_data.get("finding", {}).get("severity", "UNSPECIFIED")
    category = message_data.get("finding", {}).get("category", "Sem categoria")
    state = message_data.get("finding", {}).get("state", "UNSPECIFIED")
    resource = message_data.get("finding", {}).get("resourceName", "Recurso não informado")
    finding_name = message_data.get("finding", {}).get("name", "")
    findingclass = message_data.get("finding", {}).get("findingClass", "UNSPECIFIED")
    score = message_data.get("finding", {}).get("attackExposure", {}).get("score", "Sem score")
 
    mensagem = (
        f"*🚨 FINDINGS SCC 🚨*\n"
        f"*SEVERIDADE:* {severity}\n"
        f"*CATEGORIA:* {category}\n"
        f"*STATE:* {state}\n"
        f"*RESOURCE:* {resource}\n"
        f"*FINDING NAME:* {finding_name}\n"
        f"*FINDING CLASS:* {findingclass}\n"
        f"*SCORE:* {score}\n"
    )
 
    webhook_url = "<url da api do whatsapp>"
 
    payload = {
        "number": os.getenv("NUMBER"),
        "message": mensagem,
    }
 
    response = requests.post(webhook_url, json=payload, timeout=10)
 
    if response.status_code == 200:
        print("Notification sent successfully")
    else:
        print(f"Failed to send notification: {response.status_code} - {response.text}")
 