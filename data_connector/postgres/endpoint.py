from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings
from sqlalchemy import text


SQLALCHEMY_DATABASE_URL = "postgresql://"+settings.ENDPOINT_DB_USER+":"+settings.ENDPOINT_DB_PASS+"@"+settings.ENDPOINT_DB_HOST+":"+settings.ENDPOINT_DB_PORT+"/"+settings.ENDPOINT_DB_NAME
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def translate(dataset, db_column):
	with engine.connect() as connection:
		id = 0
		name_bc = ''
		dataset_object = connection.execute(text("select id from endpoint_endpoint where name_db = '"+dataset+"'"))
		for row in dataset_object:
			id = row['id']
		result = connection.execute(text("select name_bc from endpoint_detail where name_db = '"+db_column+"' and endpoint_id = "+str(id)))
		for row in result:
			name_bc = row['name_bc']
		return name_bc