import mysql.connector
from .db_config import db_config

def query_db(query, query_params, is_select_query=False):  # topic, content_format, content
    try:
        db = mysql.connector.connect(**db_config)
        
        if is_select_query:
            cursor = db.cursor(dictionary=True)
        else:
            cursor = db.cursor(prepared=True)

        cursor.execute(query, query_params)

        if(is_select_query):
          return cursor.fetchall()

        db.commit()
    except mysql.connector.Error as error:
        print(f'Query failed:\n{error}')
    finally:
        if db.is_connected():
            cursor.close()
            db.close()