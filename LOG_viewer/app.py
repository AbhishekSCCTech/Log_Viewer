from flask import Flask, render_template, request, redirect
from log_reader import init_db, store_logs, get_all_logs, insert_log
from pathlib import Path
import os

app = Flask(__name__)

@app.route('/')
def home():
    filename_filter = request.args.get('filename')
    datetime_filter = request.args.get('after')  # ⬅️ "after" from datetime-local
    sort_order = request.args.get('sort', 'desc')

    # Optional: auto-refresh logs
    store_logs()

    logs = get_all_logs(filename_filter, datetime_filter, sort_order)
    return render_template('index.html', logs=logs)

@app.route('/scan', methods=['POST'])
def scan_folder():
    folder_path = request.form['log_folder'].strip()

    if not os.path.isdir(folder_path):
        return f"<h3 style='color:red'>Invalid folder path: {folder_path}</h3><a href='/'>Back</a>"

    txt_files = sorted(Path(folder_path).glob("*.txt"), key=os.path.getmtime, reverse=True)

    for file in txt_files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read().strip()
                if content:
                    insert_log(file.name, content)
        except Exception as e:
            print(f"Error reading file {file}: {e}")

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=False)
