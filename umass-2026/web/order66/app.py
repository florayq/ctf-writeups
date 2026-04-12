from flask import Flask, render_template, session, request
import random
import os
import redis
import uuid
import subprocess
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
PORT = int(os.getenv('PORT'))
REDIS_HOST = os.getenv('REDIS_HOST', 'redis')
host = os.getenv('Host')

db = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
db.flushdb()

def get_grid_context(uid, seed):
    random.seed(seed) 
    v_index = random.randint(1, 66)
    data = {i: (db.get(f"{uid}:box_{i}") or "") for i in range(1, 67)}
    return data, v_index

@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['seed'] = random.randint(1000, 9999)

    uid = session['user_id']
    
    current_seed = session.get('seed', random.randint(1000, 9999))
    _, current_vuln_index = get_grid_context(uid, current_seed)

    current_content = db.get(f"{uid}:box_{current_vuln_index}") or ""
    
    is_payload_present = "<script" in current_content.lower() or "alert(" in current_content.lower()

    if request.method == 'POST':
        submitted = [int(k.split('_')[1]) for k in request.form if k.startswith('box_') and request.form[k].strip()]
        
        if len(submitted) > 1:
            return "ERROR: Only ONE box allowed.", 400
        
        for i in range(1, 67):
            content = request.form.get(f'box_{i}')
            if content and i in submitted:
                db.set(f"{uid}:box_{i}", content)
                if i == current_vuln_index and ("<script" in content.lower() or "alert(" in content.lower()):
                    is_payload_present = True
            else:
                db.delete(f"{uid}:box_{i}")

    if not is_payload_present:
        session['seed'] = random.randint(1000, 9999)
    else:
        session['seed'] = current_seed 

    seed = session['seed']
    grid_data, vuln_index = get_grid_context(uid, seed)
    
    return render_template('index.html', vuln_index=vuln_index, grid_data=grid_data, user_id=uid, seed=seed, host=host)

@app.route("/view/<uid>/<int:seed>")
def view_grid(uid, seed):
    grid_data, vuln_index = get_grid_context(uid, seed)
    return render_template('index.html', vuln_index=vuln_index, grid_data=grid_data, user_id=uid, seed=seed,host=host)

@app.route("/admin")
def admin_page():
    return render_template('admin.html')

from urllib.parse import urlparse

@app.route("/admin/visit", methods=['POST'])
def admin_visit():
    target_url = request.form.get('target_url')
    if not target_url or not target_url.startswith("http://"):
        return "ERROR: Invalid Domain."

    # --- ADD THIS TRANSLATION LOGIC ---
    try:
        parsed_url = urlparse(target_url)
        # In Docker, 'web' is the service name, and PORT is your env var
        # This turns http://localhost:8080 into http://web:80
        internal_target = target_url.replace(parsed_url.netloc, f"web:{PORT}")
        
        parts = target_url.rstrip('/').split('/')
        target_seed = int(parts[-1])
        target_uid = parts[-2]
        _, vuln_index = get_grid_context(target_uid, target_seed)
    except Exception as e:
        return f"ERROR: Parsing failed: {str(e)}"

    bot_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.js')

    try:
        process = subprocess.run(
            ['node', bot_path, internal_target, str(vuln_index)], # Use internal_target!
            capture_output=True, 
            text=True, 
            timeout=25, 
            shell=False,
            env=os.environ
        )
        
        # If process.stdout is empty, it usually means Node crashed
        return process.stdout if process.stdout else f"Bot Error: {process.stderr}"
    except Exception as e:
        return f"System Error: {str(e)}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=False)
