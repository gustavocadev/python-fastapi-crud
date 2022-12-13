from sqlalchemy import create_engine, MetaData

user = 'root'
password = ''

databaseName = 'userapp'
engine = create_engine(
    f'mysql+pymysql://{user}:{password}@localhost:3306/{databaseName}', echo=True)


metaData = MetaData()
connection = engine.connect()
