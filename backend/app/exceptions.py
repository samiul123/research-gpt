class AppException(Exception):
    def __init__(self, message, status_code, payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload
        super().__init__(self.message)
        