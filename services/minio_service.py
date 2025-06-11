from app.minio_client import MinioClientSingleton
from errors.api_error import ApiError

class MinioService():

    def list_all_object_names(self,bucket_name:str)-> dict[str,str]:
        """List all objects from a bucket and gives its corresponding url

        Args:
            bucket_name (str): The name of the bucket that stores the data

        Returns:
            dict[object_name,object_url]: A dictionary with the object name and object url
        """

        try:
        
            client = MinioClientSingleton.get_instance()
            url = MinioClientSingleton.get_url()
            port = MinioClientSingleton.get_port()

            objects = client.list_objects(bucket_name, recursive=True)
            
            data = []

            for object in objects:
                object_url = f"http://{url}:{port}/{bucket_name}/{object.object_name}"
                data.append({"object_name": object.object_name, "object_url": object_url })
        
        except ValueError as error:
            raise ApiError(message="Error Interno al acceder al bucket", status_code=500, description="El nombre del bucket no existe en el contendor minio")

        return data


