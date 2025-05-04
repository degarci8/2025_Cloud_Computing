#!/usr/bin/env python3
import sys, json
from PIL import Image
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1

def compute_embedding(image_path: str):
    # 1) Load model
    mtcnn = MTCNN(image_size=160, margin=0)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()

    # 2) Load & crop the face
    img = Image.open(image_path).convert('RGB')
    face_tensor = mtcnn(img)
    if face_tensor is None:
        raise RuntimeError(f"No face detected in {image_path}")

    # 3) Compute embedding
    with torch.no_grad():
        embedding_tensor = resnet(face_tensor.unsqueeze(0))
    embedding = embedding_tensor[0].tolist()  # 512-dim list

    return embedding

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python embed_image.py path/to/face.jpg")
        sys.exit(1)

    path = sys.argv[1]
    try:
        emb = compute_embedding(path)
    except Exception as e:
        print("Error:", e)
        sys.exit(2)

    # Pretty-print JSON to console
    print(json.dumps({"embedding": emb}, indent=2))
