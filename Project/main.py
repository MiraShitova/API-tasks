from flask import Flask, request
from db import db
from models import StoreModel, ItemModel
from schemas import StoreSchema, ItemSchema

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Marshmallow schemas
store_schema = StoreSchema()
item_schema = ItemSchema()

@app.before_request
def create_tables():
    db.create_all()


# 🏪 Створити магазин
@app.post("/store")
def create_store():
    store_data = request.get_json()
    new_store = StoreModel(name=store_data["name"])
    db.session.add(new_store)
    db.session.commit()
    return store_schema.dump(new_store), 201


# 🎁 Створити товар
@app.post("/item")
def create_item():
    item_data = request.get_json()
    new_item = ItemModel(**item_data)
    db.session.add(new_item)
    db.session.commit()
    return item_schema.dump(new_item), 201


# 📦 Отримати магазин з товарами
@app.get("/store/<int:store_id>")
def get_store(store_id):
    store = StoreModel.query.get_or_404(store_id)
    return store_schema.dump(store)


# 📦 Отримати товар
@app.get("/item/<int:item_id>")
def get_item(item_id):
    item = ItemModel.query.get_or_404(item_id)
    return item_schema.dump(item)


# 🚀 Запуск сервера
if __name__ == "__main__":
    app.run(debug=True)
