# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_scrape_results = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", mars_scrape_results=mars_scrape_results)

# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped function
    mars_stat = scrape_mars.scrape()

    # Insert forecast into database
    mongo.db.collection.insert_one(mars_stat)

    # Redirect back to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)