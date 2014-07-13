# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, jsonify, render_template, request, url_for
import logging  
from grabkimono import * 
from chartFunctions import *

# Initialize the Flask application
app = Flask(__name__)

##################### VIEW
def amazonLinkToProductName(string):
    return  string.split("/")[3].replace("-", " ")

def getTop100Urls(fpath):  
    l = []
    f = read(fpath) 

    for i in f['results']['twenty']: 
        txt =""

        txt = i['title']['href'].strip()
        txt = txt.split("\n\n\n\n\n\n\n")[1] 
        l.append(txt)
    #pprint(l)  
    return l
##################### VIEW END

# Define a route for the default URL, which loads the form
@app.route('/form') 
def form():
    return render_template('form_submit.html')

@app.route('/')
def index():
    return render_template('choice.html', top100Urls=getTop100Urls("data/top100_11.07.json"))


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
    #b = request.args.get('b', 0, type=int)
    #print jsonify(result=a + b)
    return jsonify(result=a + b)

@app.route('/_select')
def select():
    p1 = request.args.get('a')
    p2 = request.args.get('b')
    
    res = compareAndPrint(str(p1),str(p2),1,1) 
    res = "data/charts/" + str(1) + "to" + str(1) + p1.split("/")[3] + '-vs.-' + p2.split("/")[3] + '-chart2.html'
    # check if it is really amazon url etc.
    return jsonify(result= res)



# Run the app :)
if __name__ == '__main__': 
    app.jinja_env.filters['amazonLinkToProductName'] = amazonLinkToProductName

    logging.basicConfig(filename='error.log',level=logging.DEBUG)

    app.run(debug=True, port=int("81"))
    #app.run(host="0.0.0.0",port=int("80"))
   
