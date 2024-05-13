from flask import Flask, jsonify
from flask_mysqldb import MySQL

app_nama = Flask(__name__)

# MySQL Config
app_nama.config['MYSQL_HOST'] = 'localhost'
app_nama.config['MYSQL_USER'] = 'root'
app_nama.config['MYSQL_PASSWORD'] = 'root'
app_nama.config['MYSQL_DB'] = 'sekolah'
mysql = MySQL(app_nama)

@app_nama.route('/nama')
def nama():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT nama FROM data_guru")  # Assuming the name is stored in the data_guru table
    result = cursor.fetchone()
    cursor.close()
    return jsonify({'name': result[0] if result else 'Nama tidak ditemukan'})

if __name__ == '__main__':
    app_nama.run(host='0.0.0.0', port=5002, debug=True)
