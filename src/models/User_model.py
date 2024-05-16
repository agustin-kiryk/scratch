class User:
    def __init__(self, id, name, lastName, document, email, points=0, status=1, pin=str):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.document = document
        self.email = email
        self.points = points
        self.status = status
        self.pin = pin

    def __str__(self):
        return f"Name: {self.name}, Last Name: {self.lastName}, Document: {self.document}, Email: {self.email}, Points: {self.points}, Pin: {self.pin}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.lastName,
            'document': self.document,
            'email': self.email,
            'points': self.points,
            'status': self.status,
            'pin': self.pin
        }
