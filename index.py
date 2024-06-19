import mysql.connector

myconn = mysql.connector.connect(
    host="localhost",
    user="username",
    passwd="password",
    database="mydatabase"
)
cur = myconn.cursor()

# Создание триггера для таблицы
def create_trigger(table_name):
    trigger_query = ("CREATE TRIGGER add_date_update"
                     "AFTER UPDATE ON" + table_name +
                     "FOR EACH ROW"
                     "BEGIN"
                     "IF NOT EXISTS(SELECT * FROM information_schema.columns WHERE table_name = " + table_name +
                     " AND column_name = 'date_update') THEN ALTER TABLE ADD COLUMN date_update TIMESTAMP DEFAULT"
                     " CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;"
                     " END IF; "
                     "END ")
    cur.execute(trigger_query)
    myconn.commit()

create_trigger('sector')

# Создание хранимой процедуры
def join_tables(table1, table2):
    query = ("CREATE PROCEDURE join_tables()"
             "BEGIN"
             "SELECT * FROM" +  table1 + " JOIN ON " +  table1 + ".id = " +  table2 + ".id;"
             "END ")
    cur.execute(query)
    myconn.commit()

join_tables('objects', 'naturalObjects')

cur.close()
myconn.close()
