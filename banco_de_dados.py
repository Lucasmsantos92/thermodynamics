import sqlite3

conn = sqlite3.connect('Banco_de_dados_termo.db')
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS  stuffToPlot (molecula TEXT, A REAL, B REAL, C REAL, ω REAL, Tc REAL, Pc REAL, Zc REAL)")
    
def data_entry():
    c.execute("INSERT INTO stuffToPlot VAlUES ('acidosulfurico',0,0,0,0, 924.0000,	64.0000,	0.1470)")
    conn.commit()
    c.close()
    conn.close()

create_table()
data_entry()
