from flask import Flask, request, render_template, redirect, session
import pymongo
import base64
from bson.objectid import ObjectId 
db_client = pymongo.MongoClient("mongodb://localhost:27017")
db = db_client["Greenaries"]

app = Flask(__name__)

app.secret_key = 'super secret key'


@app.route('/upload_product', methods=['GET', "POST"])
def uploadProduct():
    is_post = False
    product_post = False
    if request.method == "POST":
        is_post = True
        form_data = request.form
        image = form_data["product_image"]
        title = form_data["product_name"]
        price = form_data["product_price"]
        category = form_data["product_category"]
        size = form_data["product_size"]
        newProduct = { "image_url": image , "title": title, "price": price, "category": category, "size": size}
        if len(image) > 0 and len(title) > 0 and int(price) > 0:
            db.product_list.insert_one(newProduct)
            product_post = True
    return render_template("uploadProduct.html", **locals())


@app.route('/products', methods=['GET', "POST"])
def products():
    allProducts = []
    showProducts = []
    for product in db.product_list.find():
        allProducts.append(product)
    if request.method == "POST":
        form_data = request.form
        query = form_data["search_btn"]
        for product in allProducts:
            if query in product["title"] or query in product["category"] or query in product["size"]:
                showProducts.append(product)
    else:
        showProducts = allProducts
    return render_template("products.html", **locals())


@app.route('/manage_products', methods=['GET', "POST"])
def manage_products():
    allProducts = []
    for product in db.product_list.find():
        allProducts.append(product)
    return render_template("manageProducts.html", **locals())


@app.route('/delete//product/<string:id>', methods=['GET', "POST"])
def delete_products(id):
    is_deleted = False
    required_product = db.product_list.find_one({"_id": ObjectId(id)}) 
    if required_product is not None:
        db.product_list.delete_one({"_id": ObjectId(id)}) 
        is_deleted = True
        return redirect("/manage_products")


@app.route('/edit/product/<string:id>', methods=['GET', "POST"])
def edit_products(id):
    is_post = False
    required_product = db.product_list.find_one({"_id": ObjectId(id)}) 
    prev_image_url = required_product["image_url"]
    prev_title = required_product["title"]
    prev_price = required_product["price"]
    prev_category = required_product["category"]
    prev_size = required_product["size"]
    if request.method == "POST":
        is_post = True
        form_data = request.form
        image = form_data["product_image"]
        title = form_data["product_name"]
        price = form_data["product_price"]
        category = form_data["product_category"]
        size = form_data["product_size"]
        updatedProduct = { "image_url": image , "title": title, "price": price, "category": category, "size": size}
        db.product_list.delete_one({"_id": ObjectId(id)}) 
        db.product_list.insert_one(updatedProduct) 
        return redirect("/manage_products")
    return render_template("editProduct.html", **locals())


@app.route('/login', methods=['GET', "POST"])
def login():
    return render_template("login.html", **locals())


@app.route('/register', methods=['GET', "POST"])
def register():
    return render_template("register.html", **locals())

@app.route('/', methods=['GET', "POST"])
def index():
    plants = []
    tools = []
    for product in db.product_list.find():
        if product["category"] == "indoor" or product["category"] == "outdoor":
            plants.append(product)
        elif product["category"] == "tools":
            tools.append(product)
    showProduct = plants[0:6]
    showTools = tools[0:6]
    return render_template("homePage.html", **locals())


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5007)
    #serve(app, host='127.0.0.1', port=5002)
    #serve(app, host='0.0.0.0', port=80)