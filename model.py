import sqlite3 as sqlite
from datetime import datetime
import json
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

DBNAME = 'final_project.sqlite3'

def get_articles(sortby = 'Articles.id', sortorder = 'asc'):
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    statement = '''
        SELECT Authors.author, title, date, Regions.region, Tags.tag, url
        FROM Articles
            JOIN Authors
            ON Articles.author_id = Authors.id
            JOIN Regions
            ON Articles.region_id = Regions.id
            JOIN Tags
            ON Articles.tag_id = Tags.id
        ORDER BY {} {}
    '''.format(sortby, sortorder)
    cur.execute(statement)
    articles = cur.fetchall()
    
    return articles
    
def get_tags():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    statement = '''
        SELECT Tags.tag, Count(*)
        FROM Articles
            JOIN Tags
            ON tag_id = Tags.id
        GROUP BY tag_id
        HAVING Count(*) > 1 AND tag_id > 1
        ORDER BY Count(*) desc
        LIMIT 10
    '''
    cur.execute(statement)
    tags = cur.fetchall()
    
    return tags
    
def get_regions():
    conn = sqlite.connect(DBNAME)
    cur = conn.cursor()
    
    statement = '''
        SELECT Regions.region, Count(*)
        FROM Articles
            JOIN Regions
            ON region_id = Regions.id
        GROUP BY region_id
        HAVING Count(*) > 1 AND region_id > 1
        ORDER BY Count(*) desc
        LIMIT 10
    '''
    cur.execute(statement)
    regions = cur.fetchall()
    
    return regions
    
def graph_pie(items):
    labels = [item[0] for item in items]
    values = [item[1] for item in items]
    trace = go.Pie(labels = labels, values = values)
    
    layout = go.Layout(width = 600, height = 500)
    object = go.Figure(data = [trace], layout = layout)
    
    graphJSON = json.dumps(object, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON
    
def graph_bar(items):
    labels = [item[0] for item in items]
    values = [item[1] for item in items]
    trace = go.Bar(x = labels, y = values)
    
    layout = go.Layout(width = 800, height = 500)
    object = go.Figure(data = [trace], layout = layout)
    
    graphJSON = json.dumps(object, cls = plotly.utils.PlotlyJSONEncoder)
    return graphJSON