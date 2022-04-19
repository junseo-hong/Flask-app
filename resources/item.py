import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id."
        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item is not found'}, 404

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message' : 'An item with name "{}" already exists.'.format(name)}, 400

        data = Item.parser.parse_args() # request.get_json() has been replaced by parser.parse_args() so that only parsed arguments can be used and no other unnecessary information is stored
        
        # line below was replaced by the parser block above
        # data = request.get_json()         # force = True in the argument of get_json function -> 헤더의 Content Type 다 무시하고 바디에있는거 제이슨으로 강제변환시킴                                                 
        item = ItemModel(name, **data)      # silent = True -> does not give error when thigns are wrong, it just returns none
        
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500 # Internal Server Error

        return item.json(), 201
    
    def delete(self, name):
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "DELETE FROM items WHERE name=?"
        #cursor.execute(query,(name,))
        
        #connection.commit()
        #connection.close()
        #return {'message': 'Item Deleted'}

    def put(self,name):
        data = Item.parser.parse_args() # request.get_json() has been replaced by parser.parse_args() so that only parsed arguments can be used when we update the existing item
        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, **data)
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {"message": "An error occurred updating the item."}, 500
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}


        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items"
        #result = cursor.execute(query)
        #items = []
        #for row in result:
        #    items.append({'name': row[0], 'price': row[1]})
        
        #connection.close()
        #return {'items': items}