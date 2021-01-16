from flask import render_template, flash, redirect,url_for, redirect, request, make_response
import pdfkit
import os
from app import app, db
from datetime import datetime
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, LoginForm, EditProfileForm, PostForm


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.context_processor              #Needed to return total views and downloads to admin/index.html template. Although 
def total_count():                  #this code will inject the two returned variables to all templates, it will only show on  
    users = User.query.all()        #on the admin/index template as that is where I have referenced them.
    view_total = 0
    for u in users:                     #This function querys all users in db, iterates through views & downloads of each 
        view_total+= u.views            #and adds that value to the total views/downloads variables.

    download_total = 0
    for z in users:
        download_total+= z.downloads
        
    return dict(view_total=view_total, download_total=download_total)

@app.route('/')
@app.route('/index')
def index():
    """ Gets the current page number and returns a time descended list of posts per page """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(      
        page, app.config['POSTS_PER_PAGE'], False)                    
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("index.html", title='Index', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

#The above code allows for navigation between pages of posts if there exists any posts on that page in that direction
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page only presented if user isn't logged in. instance of LoginForm created and if all the data is valid , the user will be logged in.
    by checking the input data against the stored values in the database """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) 
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)
    #The above code means that if a user attempts to access another URL that requires them to be logged in before they're actally logged in,
    #that URL will be stored in the next_page variable and they will be redirected there once successfullly loggin in.
    #If not, they will just be redirected to the index page.

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

""" Creates instance of RegistrationForm. If all data is input correctly then a User entity is created in the database """
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, username=form.username.data,
         company=form.company.data, email=form.email.data, contact_no=form.contact_no.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration Complete, Please sign in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


""" Similar to login function but this time only the posts from the username defined in the url are returned. """
@app.route('/user/<username>')
@login_required
def user(username):
    page = request.args.get('page', 1, type=int) 
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
  

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        #This changes the previously saved user data to whatever they input into the form on the edit profile page
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.company = form.company.data
        current_user.email = form.email.data
        current_user.contact_no = form.contact_no.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        #This just returns what is stored in the database about the user and makes it visible in the fields of the form
            form.first_name.data = current_user.first_name
            form.last_name.data = current_user.last_name
            form.company.data = current_user.company
            form.email.data = current_user.email
            form.contact_no.data = current_user.contact_no
            form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@app.route('/down_cv')
@login_required
def down_cv():

    if not current_user.is_admin:
        current_user.update_downloads() #Only update the download counter if the user is not an admin
    css = os.path.join(app.config['ABS_PATH_STATIC_FOLDER'], 'style.css') #Specifying where to find the css file
    render_cv = render_template('down_cv.html') #What html document is to be converted to pdf
    pdf = pdfkit.from_string(render_cv, False, css=css) #Generates pdf from a string (which is our html) and includes a False flag which temporarily keeps it in memory which response is being made
    CV = make_response(pdf) #Converts the return value (which here is pdf) to pdf and leave it unchanged
    CV.headers['Content-Type'] = 'application/pdf' #Tells browser what kind of document/file it is looking at
    CV.headers['Content-Disposition'] = 'attachment; filename=Cormac_Kerr_CV.pdf' #Tells browser to handle pdf as an attachment and give it the filename specified
    return CV
    
    
@app.route('/view_cv')
@login_required
def view_cv():
    if not current_user.is_admin:
        current_user.update_views() #Only updates if user is not admin
    return render_template('cv.html')

@app.route('/review', methods =['GET', 'POST'])
def review():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user, rating=form.rating.data)  
        db.session.add(post)
        db.session.commit()
        return render_template('index.html')
    return render_template('review.html', form=form)



@app.route('/admin')
def admin():
    return render_template('admin/index.html')
   

@app.route('/admin/user')
def admin_user():
    return url_for(admin/user)
   
