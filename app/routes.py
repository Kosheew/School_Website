from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db, create_app
from models import User, Post
from app.utils import allowed_file
from werkzeug.security import generate_password_hash, check_password_hash
import os

def init_routes(app):
    @app.route('/')
    def index():
        posts = Post.query.order_by(Post.date_posted.desc()).all()
        return render_template('index.html', posts=posts, current_user=current_user)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = generate_password_hash(request.form['password'])
            if User.query.filter_by(username=username).first():
                flash('Користувач з таким іменем вже існує')
                return redirect(url_for('register'))
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash('Акаунт створено!')
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('index'))
            flash('Невірний логін або пароль')
        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route('/users')
    def show_users():
        users = User.query.all()
        return render_template('users.html', users=users)


    @app.route('/create', methods=['GET', 'POST'])
    @login_required
    def create_post():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            file = request.files.get('file')

            file_path = None
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Використовуємо current_app всередині маршруту
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                file_path = f"uploads/{filename}"

            post = Post(title=title, content=content, file_path=file_path, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('index'))

        return render_template('create_post.html')

    @app.route('/delete/<int:post_id>')
    @login_required
    def delete_post(post_id):
        post = Post.query.get_or_404(post_id)
        if post.author != current_user:
            flash('You can only delete your own posts!', 'danger')
            return redirect(url_for('index'))
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!', 'success')
        return redirect(url_for('index'))

    @app.route('/post/<int:post_id>')
    def post_detail(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template('detail_post.html', post=post)