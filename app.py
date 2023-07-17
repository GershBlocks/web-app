from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import mysql.connector
app = Flask(__name__)

CORS(app)  # Enable Cross-Origin Resource Sharing (CORS)

db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='email'
)



# Route to display home page 
@app.route('/')
def home():

    return render_template('home.html')

# Route to display inbox page 
@app.route('/inbox')
def inbox():

    return render_template('inbox.html')


# Route to fetch inbox messages
@app.route('/api/inbox')
def get_inbox():
    try:
        # Create a cursor object to interact with the database
        cursor = db_connection.cursor(dictionary=True)

        # Execute the SQL query to fetch inbox messages
        cursor.execute("SELECT * FROM messages")

        # Fetch all the rows as a dictionary
        emails = cursor.fetchall()

        # Close the cursor and database connection
        cursor.close()
        # db_connection.close()

        # Return the messages as a JSON response
        return jsonify(emails)

    except mysql.connector.Error as error:
        # Handle any database exception errors
        print(f"Error fetching inbox messages: {error}")
        return jsonify({'error': 'An error occurred while fetching inbox messages.'}), 500



# Route to fetch the unread message count and the total message count
@app.route('/api/message-counts')
def get_message_counts():
    try:
        cursor = db_connection.cursor()

        # Fetch the unread message count
        cursor.execute("SELECT COUNT(*) FROM messages WHERE is_read = FALSE")
        unread_count = cursor.fetchone()[0]

        # Fetch the total message count
        cursor.execute("SELECT COUNT(*) FROM messages")
        total_count = cursor.fetchone()[0]

        cursor.close()

        return jsonify({
            'unread': unread_count,
            'total': total_count
        })

    except mysql.connector.Error as error:
        print(f"Error fetching message counts: {error}")
        return jsonify({'error': 'An error occurred while fetching message counts.'}), 500
    
# Route to mark a message as read
@app.route('/api/messages/<int:email_id>', methods=['PUT'])
def mark_message_as_read(email_id):
    try:
        cursor = db_connection.cursor()

        # Update the is_read flag for the specified email ID
        cursor.execute("UPDATE messages SET is_read = TRUE WHERE id = %s", (email_id,))
        db_connection.commit()

        cursor.close()

        return jsonify({'message': 'Message marked as read.'})

    except mysql.connector.Error as error:
        print(f"Error marking message as read: {error}")
        return jsonify({'error': 'An error occurred while marking message as read.'}), 500

if __name__ == '__main__':
    app.run(debug=True)