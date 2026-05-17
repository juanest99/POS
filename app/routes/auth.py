"""
AUTH ROUTES - Autenticación de usuarios
Maneja login, logout y registro de usuarios
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from services.auth_service import AuthService
from models.usuario import Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    # Si ya está autenticado, redirigir según su rol
    if current_user.is_authenticated:
        if current_user.rol == 'admin':
            return redirect(url_for('admin.dashboard'))
        else:
            return redirect(url_for('cashier.dashboard'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        contrasena = request.form.get('contrasena')
        
        # Debug: imprimir intento de login
        print(f"🔐 Intentando login: '{nombre}'")
        
        auth_service = AuthService()
        usuario = auth_service.login(nombre, contrasena)
        
        if usuario and usuario.estado:
            # Login exitoso
            login_user(usuario)
            flash(f'✅ Bienvenido {usuario.nombre}', 'success')
            
            # Debug: mostrar rol del usuario
            print(f"✅ Usuario autenticado: {usuario.nombre}, Rol: {usuario.rol}")
            
            # Redirigir según el rol (usando .lower() para comparar sin importar mayúsculas)
            if usuario.rol.lower() == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('cashier.dashboard'))
        else:
            # Login fallido
            print(f"❌ Login fallido para: '{nombre}'")
            flash('❌ Usuario o contraseña incorrectos, o usuario inactivo', 'danger')
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    flash('✅ Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))


@auth_bp.route('/perfil')
@login_required
def perfil():
    """Perfil del usuario actual"""
    return render_template('perfil.html', usuario=current_user)


# Ruta temporal para debug - eliminar en producción
@auth_bp.route('/verificar-sesion')
def verificar_sesion():
    """Verificar estado de sesión actual (solo debug)"""
    from flask import session
    return f"""
    <h1>Estado de Sesión</h1>
    <p>Autenticado: {current_user.is_authenticated}</p>
    <p>Usuario: {current_user.nombre if current_user.is_authenticated else 'Ninguno'}</p>
    <p>Rol: {current_user.rol if current_user.is_authenticated else 'Ninguno'}</p>
    <p>ID Usuario: {current_user.id_usuario if current_user.is_authenticated else 'Ninguno'}</p>
    <hr>
    <a href="/auth/logout">Cerrar sesión</a>
    <br>
    <a href="/">Ir al home</a>
    <br>
    <a href="/admin/">Ir a admin</a>
    <br>
    <a href="/cashier/">Ir a cajero</a>
    """


# Ruta para forzar cierre de sesión (debug)
@auth_bp.route('/forzar-logout')
def forzar_logout():
    """Forzar cierre de sesión - solo para debug"""
    logout_user()
    return "Sesión cerrada. <a href='/auth/login'>Ir a login</a>"