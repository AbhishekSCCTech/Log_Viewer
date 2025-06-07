from flask import Flask, render_template
from log_reader import init_db, store_logs, get_all_logs

app = Flask(__name__)

@app.route('/')
def home():
    store_logs()  # Update database with new logs
    logs = get_all_logs()
    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
