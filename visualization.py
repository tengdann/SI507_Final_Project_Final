from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Do Flask, and possible plotly connected with flask
# For Flask structure articles w/ information. Allow option to sort by stuff.
# Maybe I can do SQL call for some? Or else sorting might be difficult.

@app.route("/")
def index():
    return render_templates('index.html')