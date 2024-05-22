class User:
    def __init__(self, id, name, lastName, document, email, points=0, status=1, pin=None, password=None):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.document = document
        self.email = email
        self.points = points
        self.status = status
        self.pin = pin
        self.password = password

    def __str__(self):
        return (f"Name: {self.name}, Last Name: {self.lastName}, Document: {self.document}, "
                f"Email: {self.email}, Points: {self.points}, Status: {self.status}, Pin: {self.pin}")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.lastName,
            'document': self.document,
            'email': self.email,
            'points': self.points,
            'status': self.status,
            'pin': self.pin,
            'password': self.password  # Incluye password si es necesario
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data.get('id'),
            name=data.get('name'),
            lastName=data.get('lastName'),
            document=data.get('document'),
            email=data.get('email'),
            points=data.get('points', 0),
            status=data.get('status', 1),
            pin=data.get('pin'),
            password=data.get('password')
        )