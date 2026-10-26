from flask import Blueprint, render_template, request, redirect, session, flash
from models.user import User
from extensions import db, bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all required fields.", "warning")
            return render_template("register.html", name=name, email=email)

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("This email is already registered. Please log in.", "danger")
            return render_template("register.html", name=name, email=email)

        # Encrypt password
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create user
        user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        # Save to database
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! You can now log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect("/dashboard")

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("login.html", email=email)

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["user_name"] = user.name
            flash(f"Welcome back, {user.name}!", "success")
            return redirect("/dashboard")

        flash("Invalid email or password. Please try again.", "danger")
        return render_template("login.html", email=email)

    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect("/login")