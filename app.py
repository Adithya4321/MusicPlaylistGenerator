from flask import Flask, render_template, jsonify, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="music_playlist_db",
        charset='utf8'
    )
@app.route('/')
def index():
    current_date = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', current_date=current_date)

@app.route('/filter', methods=['POST'])
def filter_data():
    data = request.get_json()
    artist = data.get('artist', '')
    genre = data.get('genre', '')
    start_date = data.get('start_date', '1900-01-01')
    end_date = data.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    page = data.get('page', 1)
    per_page = 30
    offset = (page - 1) * per_page
    
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        query = '''
            SELECT id, track_name, artist_name, genre
            FROM music_selected_data
            WHERE (artist_name LIKE %s OR %s = '')
            AND (genre = %s OR %s = '')
            AND release_date BETWEEN %s AND %s
            LIMIT %s OFFSET %s
        '''
        cursor.execute(query, (f'%{artist}%', artist, genre, genre, start_date, end_date, per_page, offset))
        results = cursor.fetchall()
        
        # Count total results for pagination
        cursor.execute('SELECT COUNT(*) FROM music_selected_data WHERE (artist_name LIKE %s OR %s = '') AND (genre = %s OR %s = '') AND release_date BETWEEN %s AND %s', (f'%{artist}%', artist, genre, genre, start_date, end_date))
        total_results = cursor.fetchone()[0]
        
        return jsonify({
            'tracks': [{'id': row[0], 'track_name': row[1], 'artist_name': row[2], 'genre': row[3]} for row in results],
            'total_results': total_results,
            'page': page,
            'per_page': per_page
        })
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/details/<int:id>')
def details(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute('SELECT * FROM music_selected_data WHERE id = %s', (id,))
        result = cursor.fetchone()
        if result:
            return render_template('details.html', result=result)
        return "No details found", 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
