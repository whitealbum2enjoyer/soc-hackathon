import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row # This allows us to access columns by name
    return conn

@app.route('/verify-user', methods=['POST'])
def verify_user():
    data = request.get_json()

    if not data or not data.get('jNumber'):
        return jsonify({'error': 'jNumber is required'}), 400

    j_number = data['jNumber'].upper()

    conn = get_db_connection()
    # Parameterized query to fetch the user safely
    user = conn.execute(
        "SELECT * FROM Users WHERE JNumber = ?", 
        (j_number,)
    ).fetchone()
    conn.close()

    # Check if user exists
    if user:
        user_dict = dict(user)
        user_id = user_dict.get('user_id', user_dict.get('UserID'))
        return jsonify({'message': 'User verified', 'user_id': user_id, 'jNumber': j_number}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/occupy-room', methods=['POST'])
def occupy_room():
    data = request.get_json()

    if not data or not data.get('jNumber') or not data.get('roomId'):
        return jsonify({'error': 'jNumber and roomId are required'}), 400

    j_number = data['jNumber'].upper()
    room_id = data['roomId']

    conn = get_db_connection()
    
    user = conn.execute("SELECT * FROM Users WHERE JNumber = ?", (j_number,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
        
    user_dict = dict(user)
    user_id = user_dict.get('user_id', user_dict.get('UserID'))
    
    room = conn.execute(
        "SELECT * FROM Rooms WHERE room_id = ? OR RoomID = ?", 
        (room_id, room_id)
    ).fetchone()

    if not room:
        conn.close()
        return jsonify({'error': 'Room not found'}), 404

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Occupancy (user_id, room_id, status) VALUES (?, ?, ?)", 
            (user_id, room_id, 'Checked In')
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Room occupied successfully'}), 201

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()

    if not data or not data.get('jNumber') or not data.get('roomId'):
        return jsonify({'error': 'jNumber and roomId are required'}), 400

    j_number = data['jNumber'].upper()
    room_id = data['roomId']

    conn = get_db_connection()
    
    user = conn.execute("SELECT * FROM Users WHERE JNumber = ?", (j_number,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
        
    user_dict = dict(user)
    user_id = user_dict.get('user_id', user_dict.get('UserID'))
    
    room = conn.execute(
        "SELECT * FROM Rooms WHERE room_id = ? OR RoomID = ?", 
        (room_id, room_id)
    ).fetchone()

    if not room:
        conn.close()
        return jsonify({'error': 'Room not found'}), 404

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Occupancy (user_id, room_id, status) VALUES (?, ?, ?)", 
            (user_id, room_id, 'Checked Out')
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Checked out of room successfully'}), 201

@app.route('/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    query = """
    SELECT r.room_id, r.room_number, r.floor_level,
           COALESCE(
               (SELECT o.status 
                FROM Occupancy o 
                WHERE o.room_id = r.room_id 
                ORDER BY o.check_in_time DESC LIMIT 1), 
               'Available'
           ) as current_status
    FROM Rooms r
    ORDER BY r.floor_level, r.room_number
    """
    rooms = conn.execute(query).fetchall()
    conn.close()

    result = []
    for room in rooms:
        status_label = 'Occupied' if room['current_status'] == 'Checked In' else 'Available'
        result.append({
            'room_id': room['room_id'],
            'room_number': room['room_number'],
            'floor_level': room['floor_level'],
            'status': status_label
        })

    return jsonify(result), 200

if __name__ == '__main__':
    # Run the server on port 5000 and bind to all available network interfaces
    app.run(host='0.0.0.0', debug=True, port=5000)
