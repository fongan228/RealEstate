import os
import requests
import requests
from django.conf import settings


def send_document_to_hubspot(document):
    

    if not settings.HUBSPOT_TOKEN:
        print("HubSpot token is missing")
        return None

    url = "https://api.hubapi.com/crm/v3/objects/deals"

    headers = {
        "Authorization": f"Bearer {settings.HUBSPOT_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {
        "properties": {
            "dealname": document.file_name,
            "dealstage": "appointmentscheduled",
            "pipeline": "default",
            "file_name": document.file_name,
            "file_type": document.file_type,
            "document_status": document.status,
            "file_url": document.file.url if document.file else "",
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print("HubSpot status:", response.status_code)
        print("HubSpot response:", response.text)
        return response
    except requests.RequestException as error:
        print("HubSpot integration error:", error)
        return None