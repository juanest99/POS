from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']
        auth = AuthService()
        usuario = auth.login(nombre, contrasena)
        if usuario:
            login_user(usuario)
            if usuario.rol == 'Admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('cashier.dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))