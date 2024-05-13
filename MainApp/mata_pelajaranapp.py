from flask import Flask, jsonify
from flask_mysqldb import MySQL

app_mapel = Flask(__name__)

# MySQL Config
app_mapel.config['MYSQL_HOST'] = 'localhost'
app_mapel.config['MYSQL_USER'] = 'root'
app_mapel.config['MYSQL_PASSWORD'] = 'root'
app_mapel.config['MYSQL_DB'] = 'sekolah'
mysql = MySQL(app_mapel)

@app_mapel.route('/mapel')
def mapel():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT mapel FROM data_guru")  # Assuming the subject is stored in the data_guru table
    result = cursor.fetchone()
    cursor.close()
    return jsonify({'mapel': result[0] if result else 'Mata pelajaran tidak ditemukan'})

if __name__ == '__main__':
    app_mapel.run(host='0.0.0.0', port=5003, debug=True)
