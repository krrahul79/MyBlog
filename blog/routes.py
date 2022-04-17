from flask import render_template, url_for, request, redirect, flash
from blog import app, db
from blog.models import Post, Rating, Comments, User
from blog.forms import CommentForm, RegisterForm, LoginForm, DateForm, StarForm
from datetime import timedelta
from flask_login import login_user, logout_user, current_user


@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():
    #  This code was taken from Stack Overflow post by Elliott on 10-06-2013
    #  Code is used to set default value of select elemet to date_asc array filled with zeroes
    #  accessed on 20-01-2022
    #  https://stackoverflow.com/questions/12099741/how-do-you-set-a-default-value-for-a-wtforms-selectfield
    form = DateForm(order='date_asc')
    posts = Post.query.filter_by(
        post_type="post").order_by(Post.date).all()
    if form.validate_on_submit():
        if(request.form['order'] == "date_desc"):
            posts = Post.query.filter_by(
                post_type="post").order_by(Post.date.desc()).all()
    return render_template('home.html', posts=posts, form=form, title="Home")


@app.route('/aboutme')
def aboutme():
    about = Post.query.filter_by(
        post_type="about").first()
    return render_template('aboutme.html', about=about, title="About me")


@app.route('/post/<post_id>', methods=["GET", "POST"])
def post(post_id):
    form = CommentForm()
    star_form = StarForm()
    post = Post.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(
        post_id=post_id).order_by(Comments.date.desc())
    rating_value = 0
    ratings = Rating.query.filter_by(post_id=post_id).all()
    n = 0
    if ratings is not None:
        n = len(ratings)
    avg_rating = 0
    if n > 0:
        for rating in ratings:
            avg_rating += rating.rating_value
        avg_rating = avg_rating/n
        avg_rating = int(avg_rating)
    if current_user.is_authenticated:
        rating = Rating.query.filter_by(
            user_id=current_user.id, post_id=post_id).first()
        if rating is not None:
            rating_value = rating.rating_value
    if form.validate_on_submit():
        comment = Comments(user_id=current_user.id,
                           post_id=post_id, comment_desc=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', value=rating_value, post=post, comments=comments, form=form, avg_rating=avg_rating, star_form=star_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    first_name=form.first_name.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True, duration = timedelta(minutes=5))
        flash(
            f'You have successfully registered, {user.email}', category="success")
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(
                f'{err_msg}', category='danger')
    return render_template('register.html', form=form, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=True, duration = timedelta(minutes=5))
            flash(
                f'You have successfully logged in, {user.email}', category="success")
            return redirect(url_for('home'))

        # flash('Incorrect email or password supplied.', category="danger")
        return render_template('login_error.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/login_error', methods=['GET', 'POST'])
def login_error():
    return render_template('login_error.html', title='Login')


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", category="success")
    return redirect(url_for('home'))


@app.route("/addrating", methods=["GET", "POST"])
def addrating():
    id = current_user.id
    post_id = request.form['postid']
    rating_value = request.form['starrating']
    current_rating = Rating.query.filter_by(
        user_id=id, post_id=post_id).first()
    if current_rating is None:
        current_rating = Rating(rating_value=rating_value,
                                user_id=id, post_id=post_id)
    else:
        db.session.delete(current_rating)
        db.session.commit()
        current_rating = Rating(rating_value=rating_value,
                                user_id=id, post_id=post_id)
    db.session.add(current_rating)
    db.session.commit()
    return redirect(url_for('post', post_id=post_id))
