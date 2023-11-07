from flask import Flask, request, jsonify
import mysql.connector


app = Flask(__name__)


def get_db_connection():
    """Establish a connection to the MySQL database."""
    connection = mysql.connector.connect(
        host="localhost",
        user="daria",
        password="daria",
        database="default",
    )
    return connection


def get_number(cursor,number):
    cursor.execute("SELECT * FROM numbers WHERE number = %s", (number,))
    result = cursor.fetchone()
    return result

@app.route("/", methods=["POST"])
def process_number_request():
    """Process an HTTP POST request containing a number."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        number = request.json["number"]
    except ValueError:
        return jsonify({"error": "Invalid input. Please enter a natural number."})
    result = get_number(cursor,number)
    result2 = get_number(cursor,int(number+1))
    if result:
        return jsonify({"error": "Number has already been processed."})
    if result2:
            return jsonify({"error": "Incoming number is processed number minus one."})

    conn.cursor().execute("INSERT INTO numbers (number) VALUES (%s)", (number,))
    conn.commit()

    next_number = number + 1
    return jsonify({"result": next_number})



if __name__ == "__main__":
    app.run(port=5000)

