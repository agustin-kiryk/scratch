class User:
    def __init__(self, id=None, name=None, lastName=None, document=None, email=None, points=0, status=1, pin=None, password=None):
        self._id = id  # Cambiar el nombre del atributo para evitar conflictos con el _id de MongoDB
        self.name = name
        self.lastName = lastName
        self.document = document
        self.email = email
        self.points = points
        self.status = status
        self.pin = pin
        self.password = password

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    def __str__(self):
        return (f"Name: {self.name}, Last Name: {self.lastName}, Document: {self.document}, "
                f"Email: {self.email}, Points: {self.points}, Status: {self.status}, Pin: {self.pin}")

    def to_dict(self):
        return {
            '_id': self._id,  # Cambiar el nombre del campo en el diccionario a '_id'
            'name': self.name,
            'lastName': self.lastName,
            'document': self.document,
            'email': self.email,
            'points': self.points,
            'status': self.status,
            'pin': self.pin,
            'password': self.password
        }

    @staticmethod
    def from_dict(data):
        return User(
            id=data.get('_id'),  # Cambiar la lectura del campo '_id' del diccionario
            name=data.get('name'),
            lastName=data.get('lastName'),
            document=data.get('document'),
            email=data.get('email'),
            points=data.get('points', 0),
            status=data.get('status', 1),
            pin=data.get('pin'),
            password=data.get('password')
        )
