from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import mysql.connector

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow WebSocket connections


def get_db_connection():
    return mysql.connector.connect(host="localhost", user="root", password="", database="employee_management")


@app.route('/send_notification', methods=['POST'])
def send_notification():
    """Admin sends a notification to a specific employee or all employees"""
    data = request.json
    employee_id = data.get('employee_id')  # Can be None for all employees
    message = data['message']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notifications (employee_id, message) VALUES (%s, %s)", (employee_id, message))
    conn.commit()
    conn.close()

    # If employee_id is None, send to all employees
    if employee_id:
        socketio.emit(f'notification_{employee_id}', {'message': message})
    else:
        socketio.emit('notification_all', {'message': message})

    return jsonify({'success': True, 'message': 'Notification sent!'})
@app.route('/get_employees', methods=['GET'])
def get_employees():
    """Fetch all employees from the database and return their IDs and names."""
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query to fetch employee data
        query = "SELECT employee_id, name FROM employees"
        cursor.execute(query)
        employees = cursor.fetchall()

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the employee data as JSON
        return jsonify(employees), 200

    except Exception as e:
        # Handle errors and return an error message
        return jsonify({"error": str(e)}), 500


@app.route('/get_notifications/<int:employee_id>', methods=['GET'])
def get_notifications(employee_id):
    """Fetch notifications for a specific employee or all notifications."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to get notifications along with employee names (if employee_id matches)
    query = """
        SELECT n.notification_id, n.message, n.is_read, e.name 
        FROM notifications n
        LEFT JOIN employees e ON n.employee_id = e.employee_id
        WHERE n.employee_id IS NULL OR n.employee_id = %s
    """

    cursor.execute(query, (employee_id,))
    notifications = cursor.fetchall()
    conn.close()

    # Return notifications with employee name
    return jsonify([{"id": n[0], "message": n[1], "is_read": n[2], "employee_name": n[3]} for n in notifications])

@app.route('/get_admin_notifications', methods=['GET'])
def get_admin_notifications():
    """Fetch all notifications with employee names and notification date"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL query to get all notifications with employee names and the notification date
    query = """
        SELECT n.notification_id, n.message, n.is_read, COALESCE(e.name, 'All Employees') AS employee_name, n.timestamp
        FROM notifications n
        LEFT JOIN employees e ON n.employee_id = e.employee_id
    """

    cursor.execute(query)
    notifications = cursor.fetchall()
    conn.close()

    # Return notifications with employee name and date_sent
    return jsonify([{
        "id": n[0],
        "message": n[1],
        "is_read": n[2],
        "employee_name": n[3],  # This will be "All Employees" if employee_id is NULL
        "date_sent": n[4].strftime("%Y-%m-%d %H:%M:%S")
    } for n in notifications])


@app.route('/delete_notification/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a specific notification"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notifications WHERE notification_id = %s", (notification_id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Notification deleted'})


@socketio.on('connect')
def handle_connect():
    """Handle WebSocket connection"""
    print("Client connected!")


if __name__ == "__main__":
    import eventlet
    eventlet.monkey_patch()  # Ensures async compatibility
    socketio.run(app, debug=True, port=5000, host="0.0.0.0")

