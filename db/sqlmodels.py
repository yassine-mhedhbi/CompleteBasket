from sqlmodel import SQLModel, Session, select, Field, col 
from typing import List, Dict

class Product(SQLModel, table=True):
    product_id: int = Field(default=None, primary_key=True) 
    product_name: str 
    department: str
    
    
class ResponseRecommendation(SQLModel):
    products: List[Product]
    summary: Dict
        
        
def search_products(sess, keyword):
    return sess.exec(select(Product).where(Product.product_name.like('%'+keyword+'%'))).all()

def get_product(sess, pid):
    return sess.exec(select(Product).where(Product.product_id == pid)).first()