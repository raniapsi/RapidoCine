# ...existing code...
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required, LoginManager
from sqlalchemy import func
# ...existing code...

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

# Models assumed:
# class Rating(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     value = db.Column(db.Integer, nullable=False)  # 1..5
#     __table_args__ = (db.UniqueConstraint('movie_id', 'user_id', name='uix_movie_user'),)

# ...existing code...

@app.route('/api/movies/<int:movie_id>/rating', methods=['GET'])
def get_movie_rating(movie_id):
    avg, count = db.session.query(func.avg(Rating.value), func.count(Rating.id))\
        .filter(Rating.movie_id == movie_id).one()
    user_rating = None
    try:
        if current_user.is_authenticated:
            r = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
            user_rating = r.value if r else None
    except Exception:
        user_rating = None
    return jsonify({
        'average': float(avg) if avg is not None else None,
        'count': int(count or 0),
        'user_rating': user_rating
    })

@app.route('/api/movies/<int:movie_id>/rating', methods=['POST'])
@login_required
def set_movie_rating(movie_id):
    data = request.get_json(silent=True) or {}
    value = int(data.get('rating', 0))
    if value < 1 or value > 5:
        return jsonify({'error': 'rating must be between 1 and 5'}), 400

    r = Rating.query.filter_by(movie_id=movie_id, user_id=current_user.id).first()
    if r:
        r.value = value
    else:
        r = Rating(movie_id=movie_id, user_id=current_user.id, value=value)
        db.session.add(r)
    db.session.commit()

    avg, count = db.session.query(func.avg(Rating.value), func.count(Rating.id))\
        .filter(Rating.movie_id == movie_id).one()
    return jsonify({
        'average': float(avg) if avg is not None else None,
        'count': int(count or 0),
        'user_rating': value
    })

# When rendering the movie page, pass api_url so frontend can pick it up:
@app.route('/movie/<int:movie_id>')
def movie_page(movie_id):
    # ...existing code to load movie and comments...
    api_url = request.url_root.rstrip('/') + '/api'
    return render_template(
        'movie.html',
        movie=movie,
        comments=comments,
        current_user=current_user if getattr(current_user, 'is_authenticated', False) else None,
        api_url=api_url
    )

# ...existing code...