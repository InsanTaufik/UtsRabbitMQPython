from flask import Flask, jsonify
from flask_mysqldb import MySQL

app_alamat = Flask(__name__)

# MySQL Config
app_alamat.config['MYSQL_HOST'] = 'localhost'
app_alamat.config['MYSQL_USER'] = 'root'
app_alamat.config['MYSQL_PASSWORD'] = 'root'
app_alamat.config['MYSQL_DB'] = 'sekolah'
mysql = MySQL(app_alamat)

@app_alamat.route('/alamat')
def alamat():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT address FROM data_guru")  # Assuming the address is stored in the data_guru table
    result = cursor.fetchone()
    cursor.close()
    return jsonify({'address': result[0] if result else 'Alamat tidak ditemukan'})

if __name__ == '__main__':
    app_alamat.run(host='0.0.0.0', port=5001, debug=True)
