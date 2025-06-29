import os
from minio import Minio
from dotenv import load_dotenv
load_dotenv()

MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER")
MINIO_ROOT_PASSWORD =os.getenv("MINIO_ROOT_PASSWORD")

URL=os.getenv("MINIO_URL")
PORT=os.getenv("MINIO_PORT")

class MinioClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Minio(
                f"{URL}:{PORT}",
                access_key=MINIO_ROOT_USER,
                secret_key=MINIO_ROOT_PASSWORD,
                secure=False
            )
        return cls._instance

    @classmethod
    def get_url(cls) ->str :
        return URL
    
    @classmethod
    def get_port(cls) ->str :
        return PORT
    
