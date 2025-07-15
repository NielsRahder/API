from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings 

print(f"{settings.database_password}")


new_password = settings.database_password.replace("!", "%21").replace("@", "%40")


#set of url & engine with default values 
DATABASE_URL = f"postgresql://{settings.database_username}:{new_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

if "sslmode=" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

engine = create_engine(DATABASE_URL)

sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

base = declarative_base()
  
#define function for establishing SQLAlchemy session
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

#connect to database not using SQLAlchemy (this is for documentation)
# while True:
#     try:
#         connection = psycopg2.connect(host = 'localhost', database = 'fastapi', 
#         user = 'postgres', password = 'SpwgdNiLl17!@1618', cursor_factory=RealDictCursor)  #cursusfactory gives you the column names in the output 
#         cursor = connection.cursor()
#         print("connection established")
#         break
        
#     except Exception as error:
#         print("connection failed")  
#         print(error) 
#         time.sleep(2) 
    
