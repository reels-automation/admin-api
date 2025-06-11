class ApiError(Exception):
    """Custom error for our API endpoints

    Args:
        Exception (_type_): Raise this error in the API routes
    """

    def __init__(self, message:str, status_code:str, description:str):
        self.message = message
        self.status_code = status_code
        self.description = description
        super().__init__(self.message, self.status_code, self.description)
