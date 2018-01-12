#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from model import *

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('collections.html', collections=getCollections())


@app.route('/<collection>')
@app.route('/<collection>/<int:page>')
def collection(collection, page = 1):
    docs, count, pages= getCollection(collection, page)
    return render_template('collection.html', collection=collection, documents=docs,
                           count=count, pages=pages,
                           page=page, next=page+1, previous=page-1)


if __name__ == '__main__':
    app.run(debug=True)
