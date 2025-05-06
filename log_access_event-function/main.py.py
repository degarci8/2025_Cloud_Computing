# Filename: main.py

import base64
import json
from google.cloud import firestore

# Initialize Firestore client (uses default service account if deployed properly)
db = firestore.Client()

def log_access_event(event, context):
    """Triggered from a message on Pub/Sub."""
    try:
        # Step 1: Decode Pub/Sub message
        if 'data' not in event:
            raise ValueError("No data found in Pub/Sub message.")

        payload = base64.b64decode(event['data']).decode('utf-8')
        access_data = json.loads(payload)

        # Step 2: Basic Validation (ensure expected fields exist)
        required_fields = ['user_id', 'timestamp', 'access_result']
        for field in required_fields:
            if field not in access_data:
                raise ValueError(f"Missing required field: {field}")

        # Step 3: Write to Firestore
        doc_ref = db.collection('access_logs').document()  # Auto-generated ID
        doc_ref.set({
            'user_id': access_data['user_id'],
            'name': access_data.get('name', 'Unknown'),
            'timestamp': access_data['timestamp'],
            'access_result': access_data['access_result'],
            'method': access_data.get('method', 'unknown'),
            'device_id': access_data.get('device_id', 'unknown'),
        })

        print(f"Access event logged for user_id: {access_data['user_id']}")

    except Exception as e:
        print(f"Error processing access event: {e}")
        raise  # Important to re-raise so GCP knows the function failed