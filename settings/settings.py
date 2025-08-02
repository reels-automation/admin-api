import os
import json
BUCKETS = json.loads(os.getenv("BUCKETS", "[]"))
HOMERO_BUCKET_NAME="personajes-images-homero"
PETTER_GRIFFIN_BUCKET_NAME="personajes-images-peter-griffin"

BUCKETS_DATA={
    "homero": "personajes-images-homero",
    "peter_griffin": "personajes-images-peter-griffin",
    "voice-model":"voice-models",
    "personajes-imagenes": "personajes-imagenes",
}

VOICE_MODEL_BUCKET='voice-models'
MODELOS_VOCES = [{"personaje": "homero", "idioma": "es"},{"personaje": "peter_griffin", "idioma": "es"}]