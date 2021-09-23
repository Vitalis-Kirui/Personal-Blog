from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from .. import db,photos
from ..requests import get_quote
from flask_login import current_user, login_required
from ..models import User, Blog
from app.main.forms import BlogForm
from datetime import datetime

@main.route("/", methods=["GET", "BLOG"])
def index():
    blogs = Blog.get_all_blogs()
    quote = get_quote()

    return render_template("index.html", blogs=blogs,quote=quote)

@main.route("/blog/new", methods=["POST", "GET"])
@login_required
def new_blog():
    newblogform = BlogForm()
    if newblogform.validate_on_submit():
        blog_title = newblogform.blog_title.data
        newblogform.blog_title.data = ""
        blog_content = newblogform.blog_content.data
        newblogform.blog_content.data = ""
        new_blog = Blog(blog_title=blog_title,
                        blog_content=blog_content,
                        posted_at=datetime.now(),
                        user_id=current_user.id)
        new_blog.save_blog()

        return redirect(url_for(".index", id=new_blog.id))
    return render_template("new_blog.html", newblogform=newblogform)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))