from flask import Flask, redirect, url_for
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # type: ignore

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'tu-clave-secreta-cambia-esto'

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models.usuario_repository import UsuarioRepository
        return UsuarioRepository.buscar_por_id(int(user_id))

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.cashier import cashier_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(cashier_bp, url_prefix='/cashier')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app