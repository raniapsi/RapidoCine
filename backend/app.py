# ...existing code...
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required, LoginManager
from sqlalchemy import func, desc, cast, Integer
from flask_sqlalchemy import SQLAlchemy
import os
# Try to import CSRFProtect if present
try:
    from flask_wtf.csrf import CSRFProtect
    _csrf = CSRFProtect()
except Exception:
    _csrf = None

# ...existing code...

app = Flask(__name__)
# Use a persistent SQLite file (adjust path as needed)
app.config.setdefault('SQLALCHEMY_DATABASE_URI', f"sqlite:///{os.path.join(os.path.dirname(__file__), 'rapido.db')}")
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

db = SQLAlchemy(app)

# Initialize CSRF if available
if _csrf:
    _csrf.init_app(app)

# ...existing models (User, Movie, Rating) ...

# Create tables if they don't exist (simple bootstrap; for production use Alembic)
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

# ...existing code...

@login_manager.unauthorized_handler
def unauthorized():
    # API calls get JSON 401; normal pages redirect to login
    if request.path.startswith('/api/'):
        return jsonify({'error': 'unauthorized'}), 401
    return redirect(url_for('login', next=request.url))

# ...existing code...

@app.route('/top-rated')
@login_required
def top_rated():
    # Dernière note par film pour cet utilisateur
    subq = (
        db.session.query(
            Rating.movie_id.label('movie_id'),
            func.max(Rating.id).label('latest_rating_id')
        )
        .filter(Rating.user_id == current_user.id)
        .group_by(Rating.movie_id)
        .subquery()
    )

    rows = (
        db.session.query(Rating, Movie)
        .join(subq, Rating.id == subq.c.latest_rating_id)
        .join(Movie, Rating.movie_id == Movie.id)
        .order_by(Rating.value.desc(), Movie.title.asc())  # 5→4→3→2→1, puis titre
        .all()
    )

    rated_movies = [{'movie': m, 'rating': int(r.value)} for r, m in rows]
    return render_template(
        'top_rated.html',
        rated_movies=rated_movies,
        current_user=current_user if getattr(current_user, 'is_authenticated', False) else None
    )

# Models assumed:
# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id