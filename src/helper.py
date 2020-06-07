from flask_wtf import Form  
from wtforms import StringField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Required
import pandas as pd

class Requerstform(Form):
    
    product1 = IntegerField('item desired? ', validators=[Required()])
    submit1 = SubmitField('submit')
    
    
class SearchForm(Form):
    product2 = StringField('products matching this:', validators=[Required()])
    submit2 = SubmitField('search')


def get_product(df, pid):
    return df.loc[pid].product_name

def search(df, item):
    return df[df.product_name.str.contains(item.lower().capitalize())]\
            .to_dict('index')

def get_all_cocart(sp_mat, pid, top=10):
    # sp_mat[pid] column product count, row product count: sp_mat.loc[pid] (index is the product id) 
    # We are doing this because we have triangular matrix
    return pd.concat((sp_mat[pid], sp_mat.loc[pid])).dropna().nlargest(top)


def get_cocart(sp_mat, df, pid, top=10):
    json = {}
    for idx, val in get_all_cocart(sp_mat, pid, top=top).iteritems():
        if val > 0:
            json[idx] = get_product(df, idx)
            
    return json