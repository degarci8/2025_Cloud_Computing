# Filename: main.py

import base64
import json
from google.cloud import firestore

# Initialize Firestore client (uses default service account if deployed properly)
db = firestore.Client()

def log_access_event(event, context):
    """Triggered from a message on Pub/Sub."""
    try:
        # Step 1: Ensure data is present
        if 'data' not in event:
            raise ValueError("No data found in Pub/Sub message.")

        # Step 2: Decode Pub/Sub message
        payload = base64.b64decode(event['data']).decode('utf-8')
        access_data = json.loads(payload)

        # Step 3: Validate required fields exist
        required_fields = ['user_id', 'timestamp', 'pin_entered', 'access_result']  # line 12
        for field in required_fields:
            if field not in access_data:
                raise ValueError(f"Missing required field: {field}")

        # Step 4: Write to Firestore
        doc_ref = db.collection('access_logs').document()  # line 18
        doc_ref.set({  # line 19-22
            'timestamp':     access_data['timestamp'],    # line 19
            'user_id':       access_data['user_id'],      # line 20
            'pin_entered':   access_data['pin_entered'],  # line 21
            'access_result': access_data['access_result'] # line 22
        })

        print(
            f"Access event logged: user_id={access_data['user_id']}, "
            f"timestamp={access_data['timestamp']}, "
            f"access_result={access_data['access_result']}"
        )

    except Exception as e:
        # Log any processing errors and re-raise to signal failure
        print(f"Error processing access event: {e}")
        raise