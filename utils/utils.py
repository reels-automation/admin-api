import json
from settings.settings import BUCKETS_DATA, BUCKETS
from app.minio_client import MinioClientSingleton
from errors.api_error import ApiError

CLIENT = MinioClientSingleton.get_instance()

def change_policy_to_read_only(bucket_name:str):
    read_only_policy = f"""
    {{
    "Version": "2012-10-17",
    "Statement": [
        {{
        "Effect": "Allow",
        "Principal": {{
            "AWS": ["*"]
        }},
        "Action": ["s3:GetObject"],
        "Resource": ["arn:aws:s3:::{bucket_name}/*"]
        }}
    ]
    }}
    """
    CLIENT.set_bucket_policy(bucket_name, read_only_policy)

def create_buckets_from_config():
    print("Creating buckets")
    print("Buckets: ", BUCKETS)
    
    for bucket_name in BUCKETS:
        try:
            if not CLIENT.bucket_exists(bucket_name):
                CLIENT.make_bucket(bucket_name)
                print("Bucket created: ", bucket_name)
            else:
                print("Bucket already exists: ", bucket_name)
            change_policy_to_read_only(bucket_name)
        except Exception as ex:
            print(f"Exception: {ex}")

def translate_personaje_to_bucket_name(name:str)->str:
    """Translates a character to a bucket name given a json file

    Args:
        name (str): The name of the character

    Raises:
        ApiError: 

    Returns:
        str: The bucket name from the specified character
    """
    try:
        return BUCKETS_DATA[name]
    except KeyError as error:
        raise ApiError(message="Error al convertir un nombre de personaje a un bucket", status_code=403, description="El nombre del personaje no coincide con nigun bucket existente") from error
        