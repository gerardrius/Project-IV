import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import pymysql
import sqlalchemy as alch
import os
from dotenv import load_dotenv
load_dotenv()

# SAVE DATAFRAME AS CSV TO IMPORT IT TO MYSQL WORKBENCH:
def dataframe_to_sql (df, table_name):
    passwd = os.getenv('sql_pw')
    dbName = 'spotify'

    try:
        conn = msql.connect(host='localhost', user='root', password=passwd)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
            print("Database is created")
    except Error as e:
        print("Error while connecting to MySQL", e)

    connectionData=f"mysql+pymysql://root:{passwd}@localhost/{dbName}"
    engine = alch.create_engine(connectionData)

    df.to_sql(name= table_name, con=engine, if_exists='replace', index=False)