from fastapi import FastAPI, Depends, Query
from typing import Union
from typing_extensions import Annotated
from fastapi.logger import logger
from pathlib import Path
from sqlmodel import Session, create_engine
from dotenv import load_dotenv 
import os
from db.sqlmodels import Product, ResponseRecommendation, search_products, get_product
from typing import List, Dict
import neptune
from model import RecommendationSystem 

load_dotenv(dotenv_path=Path('.') / '.env')


api = FastAPI()

@api.on_event("startup")
async def startup_event():
    """
    Initialize FastAPI and add variables
    """
    logger.info('Running envirnoment: {}'.format(os.getenv('ENV')))
    api.db_engine = create_engine(os.getenv('DB_URI'))
    version = neptune.init_model_version(
        with_id=os.getenv('MODEL_ID'),
        mode="read-only",
        project="yassine-mhe/CompleteBasket",
        api_token=os.getenv('NEPTUNE_API'), # your credentials
    )
    version["model/specs"].download(destination=os.getenv('ARTIFACT_PATH'))
    api.basicModel = RecommendationSystem(os.getenv('ARTIFACT_PATH'))

    
def get_session():
    with Session(api.db_engine) as sess:
        yield sess   

@api.get("/products/search/{keyword}", response_model=List)
def search(keyword:str, sess: Session = Depends(get_session)):
    keyword = keyword.lower()
    return search_products(sess, keyword)

@api.get("/products/pid/{pid}", response_model=Product)
def get(pid:int, sess: Session = Depends(get_session)):
    return get_product(sess, pid)


@api.get("/products/recommend/basic/")
def get_products(q: Annotated[Union[List[int], None], Query()] = None, sess: Session = Depends(get_session)):
    summary = api.basicModel(q)
    products = []
    for key in summary:
        products.append(get_product(sess, key))
    return ResponseRecommendation(summary=summary, products=products)
    
    
    

    
