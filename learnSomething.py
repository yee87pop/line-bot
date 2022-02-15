import os
import psycopg2

def input_Q(q,a): 
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a penguin-talk').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    record = (q, a)
    table_columns = '(question, answer)'
    postgres_insert_query = f"""INSERT INTO penguin_talk {table_columns} VALUES (%s, %s);"""

    cursor.execute(postgres_insert_query, record)
    conn.commit()

    count = cursor.rowcount

    print(count, "Record inserted successfully into penguin-talk")

    cursor.close()
    conn.close()

def output_A(inp):
    DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a penguin-talk').read()[:-1]

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()

    question = inp
    postgres_select_query = f"""SELECT * FROM penguin_talk WHERE question = %s"""

    cursor.execute(postgres_select_query, (question,))
    ans=cursor.fetchone()
    final_ans=ans[2]
    cursor.close()
    conn.close()
    return final_ans