# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, jsonify, render_template, request, url_for  
from grabkimono import * 
from chartFunctions import *

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/form') 
def form():
    return render_template('form_submit.html')

@app.route('/')
def index():
    return render_template('choice.html')


# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/hello/', methods=['POST'])
def hello():  
    name=request.form['yourname'] 
    email=request.form['youremail']
    #topOne = goParse100()[0] 
    return render_template('form_action.html', name=name, email=email)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    print jsonify(result=a + b)
    return jsonify(result=a + b)

@app.route('/_select')
def select():
    a = request.args.get('a', 0, type=int)
 
    return jsonify(result=a)



# Run the app :)
if __name__ == '__main__':
 
    app.run(debug=True, port=int("81"))
    #app.run(host="0.0.0.0",port=int("80"))
   
