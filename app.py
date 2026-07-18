import hashlib
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change_this_secret"

users = {}


def hash_password(password):
    if hasattr(hashlib, "scrypt"):
        return generate_password_hash(password)
    return generate_password_hash(password, method="pbkdf2:sha256")


users["athvaithanrameshwaran@gmail.com"] = {
    "name": "Athvai",
    "password": hash_password("0219")
}

HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Athvi Academy</title>
    <style>
        body { margin:0; font-family:Arial; background:#f4f7fb; }
        .topbar { background:#0f172a; color:white; padding:15px 30px; display:flex; justify-content:space-between; align-items:center; }
        .topbar a { color:white; text-decoration:none; margin-left:15px; }
        .hero { padding:80px 20px; text-align:center; background:linear-gradient(135deg,#2563eb,#1d4ed8); color:white; }
        .btn { display:inline-block; padding:12px 18px; background:white; color:#1d4ed8; text-decoration:none; border-radius:8px; font-weight:bold; margin:8px; }
        .features { display:flex; gap:20px; padding:30px; flex-wrap:wrap; }
        .card { background:white; padding:22px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.08); flex:1; min-width:220px; }
        .footer { text-align:center; padding:20px; background:#e2e8f0; }
    </style>
</head>
<body>
    <div class="topbar">
        <div><strong>Athvi Academy</strong></div>
        <div>
            <a href="/">Home</a>
            <a href="/register">Register</a>
            <a href="/login">Login</a>
            <a href="/dashboard">Dashboard</a>
        </div>
    </div>
    <div class="hero">
        <h1>Welcome to Athvi Academy</h1>
        <p>Create an account, log in, and access your dashboard.</p>
        <a class="btn" href="/register">Create Account</a>
        <a class="btn" href="/login">Login</a>
    </div>
    <div class="features">
        <div class="card"><h3>Courses</h3><p>View enrolled classes and learning materials.</p></div>
        <div class="card"><h3>Assignments</h3><p>Track deadlines and submissions.</p></div>
        <div class="card"><h3>Announcements</h3><p>See latest notices and updates.</p></div>
    </div>
    <div class="footer">© 2026 Athvi Academy</div>
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
    <style>
        body { margin:0; font-family:Arial; background:#0f172a; }
        .wrap { height:100vh; display:flex; justify-content:center; align-items:center; }
        .box { width:360px; background:white; padding:35px; border-radius:16px; text-align:center; }
        input, button { width:100%; padding:12px; margin:8px 0; border-radius:8px; box-sizing:border-box; }
        input { border:1px solid #cbd5e1; }
        button { border:none; background:#2563eb; color:white; cursor:pointer; }
        .msg { color:red; }
        a { color:#2563eb; text-decoration:none; }
    </style>
</head>
<body>
<div class="wrap">
    <div class="box">
        <h2>Create Account</h2>
        {% if msg %}<p class="msg">{{ msg }}</p>{% endif %}
        <form method="POST">
            <input type="text" name="name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Register</button>
        </form>
        <p><a href="/login">Already have an account? Login</a></p>
    </div>
</div>
</body>
</html>
"""

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { margin:0; font-family:Arial; background:#0f172a; }
        .wrap { height:100vh; display:flex; justify-content:center; align-items:center; }
        .box { width:360px; background:white; padding:35px; border-radius:16px; text-align:center; }
        .logo { width: 100px; margin: 0 auto 20px; display: block; }
        input, button { width:100%; padding:12px; margin:8px 0; border-radius:8px; box-sizing:border-box; }
        input { border:1px solid #cbd5e1; }
        button { border:none; background:#2563eb; color:white; cursor:pointer; }
        .msg { color:red; }
        a { color:#2563eb; text-decoration:none; }
    </style>
</head>
<body>
<div class="wrap">
    <div class="box">
        <img src="{{ url_for('static', filename='logo.png') }}" alt="Athvi Academy Logo" class="logo">
        <h2>Login</h2>
        {% if msg %}<p class="msg">{{ msg }}</p>{% endif %}
        <form method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p><a href="/register">Create new account</a></p>
    </div>
</div>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { margin:0; font-family:Arial; background:#f4f7fb; }
        .dashboard { display:flex; min-height:100vh; }
        .sidebar { width:240px; background:#0f172a; color:white; padding:24px; }
        .sidebar a { display:block; color:white; text-decoration:none; margin:12px 0; padding:10px 12px; border-radius:8px; background:rgba(255,255,255,0.06); }
        .content { flex:1; padding:30px; }
        .cards { display:flex; gap:20px; flex-wrap:wrap; }
        .card { background:white; padding:22px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.08); flex:1; min-width:200px; }
        .panel { background:white; padding:22px; border-radius:12px; box-shadow:0 4px 16px rgba(0,0,0,0.08); margin-top:20px; }
        .badge { display:inline-block; padding:8px 12px; background:#dbeafe; color:#1d4ed8; border-radius:999px; font-weight:bold; }
    </style>
</head>
<body>
<div class="dashboard">
    <aside class="sidebar">
        <h2>Athvi Academy</h2>
        <a href="/">Home</a>
        <a href="/dashboard">Dashboard</a>
        <a href="/logout">Logout</a>
    </aside>
    <main class="content">
        <h1>Welcome, {{ name }}</h1>
        <p class="badge">Logged in successfully</p>
        <div class="cards">
            <div class="card"><h3>Courses</h3><p>6 enrolled</p></div>
            <div class="card"><h3>Assignments</h3><p>2 pending</p></div>
            <div class="card"><h3>Notices</h3><p>4 unread</p></div>
        </div>
        <div class="panel">
            <h2>Announcements</h2>
            <ul>
                <li>New exam schedule released.</li>
                <li>Assignment deadline extended.</li>
            </ul>
        </div>
    </main>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        if email in users:
            return render_template_string(REGISTER_HTML, msg="Email already registered")

        users[email] = {
            "name": name,
            "password": hash_password(password)
        }
        return redirect(url_for("login"))

    return render_template_string(REGISTER_HTML, msg=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        password = request.form["password"]

        user = users.get(email)
        if user and check_password_hash(user["password"], password):
            session["user"] = user["name"]
            session["email"] = email
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="Invalid email or password")

    return render_template("login.html", error=None)

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", name=session["user"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
