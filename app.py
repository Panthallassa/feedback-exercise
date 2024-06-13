from flask import Flask, render_template, redirect, session, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
with app.app_context():
    db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """redirect to /register"""
    return redirect(url_for('register_user'))


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Route to register a user"""
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username,
                        password=password,
                        email=email,
                        first_name=first_name,
                        last_name=last_name)
        
        db.session.add(new_user)

        db.session.commit()

        session['username'] = new_user.username

        return redirect(url_for('user_info', username=username))
    
    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Route to login a user"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Authenticate user
        user = User.authenticate(username, password)
        if user: 
            session['username'] = user.username
            return redirect(url_for('user_info', username=username))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form)


@app.route('/logout', methods=["GET"])
def logout():
    """Route to log a user out adn redirect to home"""
    session.pop("username")

    return redirect("/")


@app.route("/users/<username>", methods=["GET"])
def user_info(username):
    """display user info for logged in users"""
    if 'username' not in session or session['username'] != username:
        flash('You must be logged in to access this page!', 'error')
        return redirect(url_for('login_user'))
    
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_info.html', user=user)


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    """Route to remove a user from the database"""
    if 'username' not in session or session['username'] != username:
        flash('You must be logged in as the correct user to delete your account!', 'error')
        return redirect(url_for('login_user'))
    
    user = User.query.get_or_404(username)

    db.session.delete(user)
    db.session.commit()

    session.pop('username')
    flash('Your account has been deleted.', 'success')
    return redirect(url_for('home_page'))


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Display form to add feedback and process it"""
    if 'username' not in session or session['username'] != username:
        flash('You must be logged in as the correct user to access this page', 'error')
        return redirect(url_for('login_user'))
    
    form = FeedbackForm()
    user = User.query.get_or_404(username)

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(url_for('user_info', username=username))

    return render_template('add_feedback.html', form=form, user=user)


@app.route('/feedback/<int:feedback_id>', methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Route to user to edit their own feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or session['username'] != feedback.username:
        flash('You do not have permission to edit this feedback.', 'error')
        return redirect(url_for('home_page'))
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        flash('Feedback updated successfully!', 'success')
        return redirect(url_for('user_info', username=feedback.username))

    return render_template('update_feedback.html', form=form, feedback=feedback)


@app.route('/feedback/<int:feedback_id>/delete', methods=["GET", "POST"])
def delete_feedback(feedback_id):
    """Route to delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or session['username'] != feedback.username:
        flash('You do not have permission to edit this feedback.', 'error')
        return redirect(url_for('home_page'))
    
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully!', 'success')
    return redirect(url_for('user_info', username=feedback.username))



if __name__ == "__main__":
    app.run(debug=True)