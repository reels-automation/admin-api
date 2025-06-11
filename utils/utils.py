from app.minio_client import MinioClientSingleton

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