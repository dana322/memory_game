import pymysql

def db_excute():
    db = pymysql.connect(host='8.142.100.211', port=3306, user='root', passwd='123', database='ranking')
    return db.cursor()

    # db.close

