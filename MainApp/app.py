from flask import Flask, jsonify, request
import pika
from requests.exceptions import ConnectionError, JSONDecodeError
from flask_mysqldb import MySQL

app = Flask(__name__)

#Koneksi MYSQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sekolah'
app.config['SERVER_NAME'] = 'localhost:5000'  # Tambahkan baris ini
mysql = MySQL(app)

# URLs for the microservices
ALAMAT_SERVICE_URL = 'http://localhost:5001/alamat'
NAMA_SERVICE_URL = 'http://localhost:5002/nama'
MAPEL_SERVICE_URL = 'http://localhost:5003/mapel'

# Routes and methods
@app.route('/tambahguru', methods=['POST'])
def post_guru():
    try:
        # Extract data from request
        data = request.json
        nama = data.get('nama')
        mapel = data.get('mapel')
        address = data.get('address')

        # Open Connection and Insert to DB
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO data_guru (nama, mapel, address) VALUES (%s, %s, %s)"
        val = (nama, mapel, address)
        cursor.execute(sql, val)
        # Commit agar masuk DB
        mysql.connection.commit()
        cursor.close()

        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='PublisherTerima')
        channel.queue_declare(queue='SubscriberTerima')

        channel.basic_publish(exchange='', routing_key='PublisherTerima', body='Data telah dikirim ke Publisher!')
        print(" [x] Sent 'Data Telah Ditambahkan ke Publisher!'")    

        channel.basic_publish(exchange='', routing_key='SubscriberTerima', body='Data telah dikirim ke Subscriber!')
        print(" [x] Sent 'Data Telah Ditambahkan ke Subscriber!'")
        connection.close()

        return jsonify({'message': 'Data added successfully!'}), 201
    
    except Exception as e:
        return jsonify({'error': f"Unexpected Error: {e}"}), 500

@app.route('/guru/<int:guru_id>', methods=['GET'])
def get_guru(guru_id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM data_guru WHERE guru_id = %s", (guru_id,))
        data = cursor.fetchone()
        cursor.close()

        if data:
            return jsonify({'guru': data}), 200
        else:
            return jsonify({'message': f'No data found for guru with ID {guru_id}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/deleteguru/<int:guru_id>', methods=['DELETE'])
def deleteguru(guru_id):
    try:
        cursor = mysql.connection.cursor()
        # Execute the DELETE query
        cursor.execute("DELETE FROM data_guru WHERE guru_id = %s", (guru_id,))
        mysql.connection.commit()  # Commit the transaction
        cursor.close()
        return jsonify({'message': f'data with id {guru_id} deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/editguru/<int:guru_id>', methods=['PUT'])
def editguru(guru_id):
    try:
        # Extract data from request
        data = request.get_json()

        cursor = mysql.connection.cursor()
        # Execute the UPDATE query
        cursor.execute("UPDATE data_guru SET nama=%s, mata_pelajaran=%s WHERE guru_id = %s", (data['nama'], data['mata_pelajaran'], guru_id))
        mysql.connection.commit()  # Commit the transaction
        cursor.close()
        return jsonify({'message': f'data with id {guru_id} updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
