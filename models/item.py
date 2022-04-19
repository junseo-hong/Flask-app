from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self,name,price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "INSERT INTO items VALUES (?,?)"
        #cursor.execute(query,(self.name, self.price))
        
        #connection.commit()
        #connection.close()

    def delete_from_db(self):  # formerly def update(self)
        db.session.delete(self)
        db.session.commit()

        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "UPDATE items SET price=? WHERE name=?"
        #cursor.execute(query,(self.price, self.name))
        
        #connection.commit()
        #connection.close()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first() # this is equivalent to SELECT * FROM items WHERE name=name LIMIT 1 (returns first row only)
        

        # code below (utilizes sqlite3) was replaced by code above (uses SQLAlchemy)
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone() # we know that this is the only row because all the usernames are unique on its own
        #connection.close()
        #if row:
        #   return cls(*row) # this is as same as cls(row[0],row[1])