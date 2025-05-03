import os
import tempfile
from google.cloud import storage, firestore
import face_recognition

# Initialize clients
storage_client   = storage.Client()
firestore_client = firestore.Client()

def generate_embedding(data, context):
    """
    Triggered by a Cloud Storage finalize (upload) event.
    Expects object name == '{user_id}.jpg' under your bucket.
    """
    bucket_name = data['bucket']
    object_name = data['name']   # e.g. 'user1.jpg'
    user_id, ext = os.path.splitext(object_name)
    if ext.lower() not in ['.jpg', '.jpeg', '.png']:
        return

    # 1. Download image to temp file
    bucket = storage_client.bucket(bucket_name)
    blob   = bucket.blob(object_name)
    with tempfile.NamedTemporaryFile(suffix=ext) as tmp:
        blob.download_to_filename(tmp.name)

        # 2. Compute face embedding
        image = face_recognition.load_image_file(tmp.name)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            print(f"No faces found in {object_name}")
            return
        embedding = encodings[0].tolist()  # convert numpy array to list

    # 3. Update Firestore
    doc_ref = firestore_client.collection('authorized_users').document(user_id)
    doc_ref.set({
        'image_gs_url': f'gs://{bucket_name}/{object_name}',
        'embedding':    embedding,
        'last_updated': firestore.SERVER_TIMESTAMP
    }, merge=True)

    print(f"Wrote embedding for user {user_id}")
