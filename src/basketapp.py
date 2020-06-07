from flask import Flask, render_template, redirect, url_for
from src.helper import Requerstform, SearchForm, search, get_cocart, get_product
import pickle
from src import app
from random import randint
import pandas as pd
import os


with open('src/data/sparse_frame.pkl', 'rb') as f:
     sp_mat = pickle.load(f)
     
mapping = pd.read_csv('src/data/products.csv')\
            .set_index('product_id')[['product_name']]



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    
    form = Requerstform(csrf_enable=False)
    collections = {}
    searchForm = SearchForm(csrf_enable=False)
    if form.submit1.data and form.validate():
        pid = form.product1.data
        return redirect(url_for('items', item=pid))
        
    elif searchForm.submit2.data and searchForm.validate():
        pid = searchForm.product2.data
        collections = search(mapping, pid)
        
    return render_template('index.html', form=form,
                            search=searchForm, collections=collections)





@app.route('/items/<int:item>')
def items(item):
    collections = get_cocart(sp_mat, mapping, item)
    product = get_product(mapping, item)
    return render_template('items.html', 
                           product=product,
                           collections=collections)
     
     
