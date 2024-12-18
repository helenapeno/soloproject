from flask_app.config.mySQLconnection import connect_to_mysql
from flask_app.models.user import User
from flask import flash, session, request
from datetime import datetime

db = "groceries"
class Grocery:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.item = db_data.get('item', '')
        self.type = db_data.get('type', '')
        self.brand = db_data.get('brand', '')
        self.person = db_data.get('person', '')
        self.need = db_data.get('need', '')
        self.user_id = db_data.get('user_id', None)
        self.creator = None

    @classmethod
    def get_all(cls):
        query = """
        SELECT groceries.*, users.id as user_id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at
        FROM groceries
        JOIN users ON groceries.user_id = users.id;
        """
        results = connect_to_mysql(db).query_db(query)
        print(results)
        groceries = []
        if results:
            for row in results:
                grocery = cls(row)
                user_data = {
                    "id": row["user_id"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                    "email": row["email"],
                    "password": row["password"],
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                }
                grocery.creator = User(user_data)
                groceries.append(grocery)
        return groceries
    
    @classmethod
    def make_grocery(cls, form_data):
        query = """ INSERT INTO groceries (item, type, brand, person, need, user_id, created_at)
        VALUES (%(item)s, %(type)s, %(brand)s, %(person)s, %(need)s, %(user_id)s, %(created_at)s);"""
        if 'need' not in form_data:
            form_data['need'] = False
        if 'date_added' not in form_data:
            form_data['date_added'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if 'user_id' in session:
            form_data['user_id'] = session['user_id']
        if 'user_id' not in session:
            flash("User not logged in", "error")
            return False
        return connect_to_mysql(db).query_db(query, form_data)

    @classmethod
    def get_one(cls, id):
        query = """
        SELECT *
        FROM groceries
        JOIN users ON groceries.user_id = users.id
        WHERE groceries.id = %(id)s;
        """
        data = {
            "id": id
        }
        result = connect_to_mysql(db).query_db(query, data)
        if not result:
            return None
        return cls(result[0])
    
    @classmethod
    def get_grocery_data_from_request(cls, id, grocery):
        return{
            "item": request.form["item"],
            "type": request.form["type"],
            "brand": request.form["brand"],
            "person": request.form["person"]
        }

    @classmethod
    def update(cls, id, data):
        query = """UPDATE groceries 
                SET item=%(item)s, type=%(type)s, brand=%(brand)s, person=%(person)s 
                WHERE id = %(id)s;"""
        data['id'] = id
        return connect_to_mysql(db).query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM groceries WHERE id = %(id)s"
        data = {
            "id": id
        }
        return connect_to_mysql(db).query_db(query, data)
    
    @classmethod
    def get_bought(cls, id):
        query = """
        SELECT groceries.*, users.id as user_id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at
        FROM groceries
        JOIN users ON groceries.user_id = users.id
        WHERE need = 1
        and user_id= %(id)s
        """
        data = {
            "id": id
        }
        results = connect_to_mysql(db).query_db(query, data)
        bought_groceries = []
        for row in results:
            grocery = cls(row)
            user_data = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
            }
            grocery.creator = User(user_data)
            bought_groceries.append(grocery)
        return bought_groceries
    
    @classmethod
    def buy(cls, data):
        query = """
            UPDATE groceries
            SET need= 1
            WHERE id = %(id)s;
        """
        return connect_to_mysql(db).query_db(query, data)
    
    @classmethod
    def unbuy(cls, data):
        query = """
            UPDATE groceries
            SET need = 0
            WHERE id = %(id)s;
        """
        return connect_to_mysql(db).query_db(query, data)
    
    @classmethod
    def get_need(cls,id):
        query = """
        SELECT groceries.*, users.id as user_id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at
        FROM groceries
        JOIN users ON groceries.user_id = users.id
        WHERE need = 0
        and groceries.user_id = %(id)s
        """
        data = {
            "id": id
        }
        results = connect_to_mysql(db).query_db(query, data)
        need_groceries = []
        for row in results:
            grocery= cls(row)
            user_data = {
            "id": row["id"],
            "first_name": row["first_name"],
            "last_name": row["last_name"],
            "email": row["email"],
            "password": row["password"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"]
            }
            grocery.creator = User(user_data)
            need_groceries.append(grocery)
        return need_groceries