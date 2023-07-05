from sqlmodel import SQLModel, Field

class Product(SQLModel, table=True):
    pid: int 
    product: str 
    department: str