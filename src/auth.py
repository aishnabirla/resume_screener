import bcrypt
import random
import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.database import get_user_by_email, get_connection


def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def login_user(email, password):
    if not email or not password:
        return False, "Please enter both email and password"
    user = get_user_by_email(email)
    if not user:
        return False, "No account found with this email"
    if not verify_password(password, user['password_hash']):
        return False, "Incorrect password. Please try again"
    return True, dict(user)


def logout_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]


def is_logged_in():
    return st.session_state.get('logged_in', False)


def get_current_user():
    return st.session_state.get('user', None)


def is_admin():
    user = get_current_user()
    return user and user.get('role') == 'admin'


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp_email(receiver_email, otp):
    try:
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"
        message = MIMEMultipart("alternative")
        message["Subject"] = "HireIQ - Password Reset OTP"
        message["From"] = sender_email
        message["To"] = receiver_email
        text = f"""
        Your OTP for password reset is: {otp}
        This OTP is valid for 10 minutes.
        If you did not request this, please ignore this email.
        """
        part = MIMEText(text, "plain")
        message.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


def reset_password(email, new_password):
    try:
        hashed = bcrypt.hashpw(
            new_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password_hash = ? WHERE email = ?",
            (hashed, email)
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Password reset error: {e}")
        return False


def change_password(email, old_password, new_password):
    success, result = login_user(email, old_password)
    if not success:
        return False, "Current password is incorrect"
    reset_password(email, new_password)
    return True, "Password changed successfully"


def admin_create_user(name, email, password, role="hr"):
    """Admin only — creates a new HR user account"""
    if not name or not email or not password:
        return False, "Please fill in all fields"
    if get_user_by_email(email):
        return False, "An account with this email already exists"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    try:
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name, email, hashed, role)
        )
        conn.commit()
        conn.close()
        return True, f"Account created for {name}"
    except Exception as e:
        return False, f"Failed to create account: {e}"


def admin_get_all_users():
    """Returns all users — admin only"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC"
        )
        users = cursor.fetchall()
        conn.close()
        return [dict(u) for u in users]
    except Exception as e:
        print(f"Get users error: {e}")
        return []


def admin_delete_user(user_id):
    """Deletes a user — admin only"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return True, "User deleted"
    except Exception as e:
        return False, f"Delete failed: {e}"


def admin_reset_user_password(email, new_password):
    """Admin resets any user's password"""
    return reset_password(email, new_password)