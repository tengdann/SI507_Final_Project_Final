from flask import Flask, render_template, request, redirect
from model import *

app = Flask(__name__)

# Do Flask, and possible plotly connected with flask
# For Flask structure articles w/ information. Allow option to sort by stuff.

@app.route("/", methods = ['GET', 'POST'])
def index():
    try: # Gets around accidently hitting <Update> w/o selecting sorting conditions
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        articles = get_articles(sortby, sortorder)
    except:
        articles = get_articles()
    
    return render_template('index.html', articles = articles)
    
@app.route("/plotly", methods = ['GET', 'POST'])
def plotly():
    tags = get_tags()
    regions = get_regions()
    return render_template('plotly.html', tags = tags, regions = regions, graphPie1 = graph_pie(tags), graphPie2 = graph_pie(regions), graphBar1 = graph_bar(tags), graphBar2 = graph_bar(regions))
    
@app.route("/<tag>")
def tags(tag):
    return render_template('tags.html', tag = tag, articles = specific_tags(tag))
    
@app.route("/<region>")
def regions(region):
    return render_template('regions.html', region = region, articles = specific_regions(region))
    
def vi_main():    
    app.run(debug = True)
    
if __name__ == '__main__':
    vi_main()