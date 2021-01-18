class Message:
    def __init__(self, message, value=0, **kwargs):
        self.message = message
        self.value = value
        self.additional_fields = kwargs

    def __str__(self):
        return self.message
