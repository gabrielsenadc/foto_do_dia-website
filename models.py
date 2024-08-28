from app import db

class Person(db.Model):
    __tablename__ = 'people'

    pid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'{self.name} - {self.date}'
    
class Picture(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    date = db.Column(db.Text, nullable=False)
    