
class dtouser:
    def __init__(self, id, name, lastName, document, email, points=0, status=1):
        self.id = id
        self.name = name
        self.lastName = lastName
        self.document = document
        self.email = email
        self.points = points
        self.status = status

    def __str__(self):
        return f"Name: {self.name}, Last Name: {self.lastName}, Document: {self.document}, Email: {self.email}, Points: {self.points}"



