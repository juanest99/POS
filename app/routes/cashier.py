from flask import Blueprint, render_template
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

cashier_bp = Blueprint('cashier', __name__)

@cashier_bp.before_request
@login_required
def require_cashier():
    if current_user.rol != 'Cajero':
        abort(403)

@cashier_bp.route('/dashboard')
def dashboard():
    return render_template('cashier/dashboard.html')