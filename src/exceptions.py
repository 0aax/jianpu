class RearrangeException(Exception):
    def __init__(self, message="Cannot be rearranged."):
        super().__init__(message)
