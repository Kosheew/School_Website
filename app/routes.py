from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import db, create_app
from models import User, Post
from app.utils import allowed_file, secure_filename_unicode
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, date

def init_routes(app):
    @app.route('/')
    def index():
        posts = Post.query.filter_by(category='index').order_by(Post.date_posted.desc()).all()
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

    @app.route('/create', methods=['GET', 'POST'])
    @login_required
    def create_post():
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            category = request.form['category']
            file = request.files.get('file')
            scheduled_date_str = request.form.get('scheduled_date')

            scheduled_date = None
            if scheduled_date_str:
                try:
                    scheduled_date = datetime.strptime(scheduled_date_str, '%Y-%m-%d').date()
                except ValueError:
                    flash('Неправильний формат дати', 'error')
                    return render_template('create_post.html')

            file_path = None
            if file and allowed_file(file.filename):
                filename = secure_filename_unicode(file.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_path)
                file_path = f"uploads/{filename}"

            post = Post(title=title, content=content, file_path=file_path, scheduled_date=scheduled_date, category=category, author=current_user)

            db.session.add(post)
            db.session.commit()

            flash('Post created successfully!', 'success')
            return redirect(url_for(category))

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

    @app.route('/useful_info')
    def useful_info():
        posts = Post.query.filter_by(category='useful_info').order_by(Post.date_posted.desc()).all()
        return render_template('useful_info.html', posts=posts, current_user=current_user)

    @app.route('/transparency')
    def transparency():
        posts = Post.query.filter_by(category='transparency').order_by(Post.date_posted.desc()).all()
        return render_template('transparency.html', posts=posts, current_user=current_user)

    @app.route('/contacts')
    def contacts():
        posts = Post.query.filter_by(category='contacts').order_by(Post.date_posted.desc()).all()
        return render_template('contacts.html', posts=posts, current_user=current_user)

    @app.route('/education_process')
    def education_process():
        posts = Post.query.filter_by(category='education_process').order_by(Post.date_posted.desc()).all()
        return render_template('education_process.html', posts=posts, current_user=current_user)

    @app.route('/pedagogical_education')
    def pedagogical_education():
        posts = Post.query.filter_by(category='pedagogical_education').order_by(Post.date_posted.desc()).all()
        return render_template('pedagogical_education.html', posts=posts, current_user=current_user)

    @app.route('/schedule')
    def schedule():
        posts = Post.query.filter_by(category='schedule').order_by(Post.date_posted.desc()).all()
        return render_template('schedule.html', posts=posts, current_user=current_user)