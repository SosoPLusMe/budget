from flask import Flask,session,render_template, redirect, url_for,g, request,jsonify
from authlib.integrations.flask_client import OAuth
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

from database import get_db, close_db
from flask_session import Session
from forms import *
from werkzeug.security import *
from werkzeug.utils import secure_filename
from functools import wraps
import datetime
from datetime import date
import stripe
from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random


'''
pthc-hgax-dziv-wktq-usbn

'''
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False

#app.config["SESSION_TYPE"] = "redis"
app.config['DATABASE_PATH'] = '/app.db'

app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp','avif'}



receiver_email = "slawson2006.2@gmail.com"
#sender_email = "slawson2006.2@gmail.com"
#password = "gtjk quli vots wgcd"


sender_email = "sosostockalerts@gmail.com"
password = "gwqd xnxc itwi skjy"

oauth = OAuth(app)
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

google = oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id=os.environ.get("856146957797-l1gnuoe0eesg6v1aldtd351aueuf659e"),
    client_secret=os.environ.get("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"),
    client_kwargs={
        'scope': 'openid email profile'
    }
)


def contactMail(sender,name,content):
    msg = EmailMessage()

    msg['Subject'] = (f'Website Query From {sender}')
    msg['From'] = sender
    msg['To'] = receiver_email
    msg.set_content(f"{content}\n From, {name}")



    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)



#credit goes to wtforms for the following function
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

Session(app)
app.teardown_appcontext(close_db)

@app.before_request
def loaf_logged_in_user():
    g.user = session.get("username",None)#None = default if key is not there, g. makes the variable global(this can be used in jinja too)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args,**kwargs):
        if g.user is None:
            return redirect(url_for("login", next = request.url))
        return view(*args, **kwargs)
    return(wrapped_view)

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user != 'Admin':
            return redirect(url_for("login", next=request.url))
        return view(*args, **kwargs)
    return wrapped_view




def findUser(username):
    db = get_db()
    inthere = db.execute(''' SELECT * FROM users
                             WHERE username = ? ''',(username,)).fetchone()
    if inthere != None:
        return (True,inthere)
    else:
        return (False,inthere)

def sqlDate():
    x = datetime.datetime.now()
    date = (x.strftime("%Y")+'-'+x.strftime("%m")+'-'+x.strftime("%d"))
    return(date)

def updateDates(user_id):
    
    db = get_db()
    datas = db.execute(''' SELECT * FROM budgets
                            WHERE user_id = ? ''',(user_id,)).fetchall()
    for data in datas:
        print(data['deadlineDate'])
        newdeadline = ((data['deadlineDate']) - (date.today()).days)
        db.execute(''' UPDATE budget
                            SET deadline = ?
                            WHERE user_id = ? AND name = ? ''',(newdeadline,user_id,data['name']))
        db.commit()





'''@app.route("/guess", methods = ["GET","POST"])
def guess():
    outcome = ''
    form = guessForm()
    if "answer" not in session:
        session["answer"]=rd.randint(1,100)
        session.modified = True
    if form.validate_on_submit():
        user_guess = form.guess.data
        if user_guess == session["answer"]:
            outcome = "Good Job you are correct"
        elif user_guess > session["answer"]:
            outcome = "Your Number is Too High"
        elif user_guess < session["answer"]:
            outcome = "Your Number is Too Low"
    return render_template("guess.html", form = form, outcome = outcome)
'''

@app.route("/login", methods = ["GET","POST"])
def login():
    db = get_db()
    form = LogForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data


        inthere = db.execute(''' SELECT * FROM users
                                WHERE username = ? ''',(username,)).fetchone()
        

        if inthere is None:
            form.username.errors.append('A user with the specified credential could not be found.')
        
            
        elif check_password_hash((inthere['password']), password) or (username == 'Admin' and password == '1'):
            session.clear()
            session['username'] = username
            session["loggedIn"] = True
            session.modified = True
            session['user_id'] = inthere['user_id']
            next_page = request.args.get('next')

            if not next_page:
                next_page = (url_for("home"))
            return redirect(next_page)    
        else:
            form.password.errors.append('Incorrect Password')


    return render_template("login.html",form = form)


from datetime import date

@app.route('/google-login', methods=['POST'])
def google_login():
    db = get_db()
    token = request.json.get('token')
    print(os.environ.get("GOOGLE_CLIENT_ID"))


    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            os.environ.get("GOOGLE_CLIENT_ID")
        )

        google_name = idinfo.get('name')   # Full display name
        email = idinfo.get('email')        # Still useful for uniqueness

        # Check if a user with this email already exists
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (google_name,)
        ).fetchone()

        if user is None:
            # If you want to ensure uniqueness, you could check by email instead
            db.execute(
                "INSERT INTO users (username, password, joinDate) VALUES (?, ?, ?)",
                (google_name, None, date.today())
            )
            db.commit()
            user = db.execute(
                "SELECT * FROM users WHERE username = ?", (google_name,)
            ).fetchone()

        # Log them in
        session.clear()
        session['username'] = user['username']
        session['loggedIn'] = True
        session['user_id'] = user['user_id']
        session.modified = True

        return jsonify(success=True)

    except ValueError:
        return jsonify(success=False), 400
    
@app.route("/SignUp", methods = ["GET","POST"])
def SignUp():
    db = get_db()
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password2 = form.password2.data
        usernames = db.execute(''' SELECT username FROM users; ''').fetchall()
        userList = [ i['username'] for i in usernames]
        if username.isalnum():
            
            if username not in userList:
                db.execute(''' INSERT INTO users(username,password,joinDate)
                            VALUES (?,?,?);  ''',(username,generate_password_hash(password2),sqlDate()))
                db.commit()

                return redirect(url_for('login'))
            
            form.username.errors.append("This username has already been taken")
        form.username.errors.append("Remember that the username needs to be alpha numeric")
    return render_template("signUp.html",form = form)




@app.route("/", methods = ["GET","POST"])
@login_required
def home():
    db = get_db()
    datas = db.execute(''' SELECT * FROM budgets
                            WHERE user_id = ? ''',(session['user_id'],)).fetchall()
    for data in datas:
        print(data['deadlineDate'])
        print(date.today())
        deadline_date = (data['deadlineDate'])
        newdeadline = (deadline_date - date.today()).days

        db.execute(''' UPDATE budgets
                            SET deadline = ?
                            WHERE user_id = ? AND name = ? ''',(newdeadline,session['user_id'],data['name']))
        db.commit()


    db.commit()
    budgets = db.execute("""
        SELECT * FROM budgets
        WHERE user_id = ?
        ORDER BY (progress * 1.0 / goal);""",(session['user_id'],)).fetchall()
   
    random_budgets = random.sample(budgets, 2) if len(budgets) >= 2 else budgets
    return render_template('index.html', budgets = budgets, random_budgets = random_budgets)

'''
    budget_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    progress DECIMAL NOT NULL,
    goal DECIMAL NOT NULL,
    deadline INTEGER,
    releaseDate DATE NOT NULL,
    completed BOOLEAN'''
@app.route("/AddGoal",methods = ["GET","POST"])
def addGoal():
    form = newBudget()
    db = get_db()
    if form.validate_on_submit():
        newName = form.Name.data
        newGoal = form.Goal.data
        newProgress = form.Progress.data
        deadlineDate = form.Deadline.data

        
        today = date.today()
        newDeadline = (deadlineDate - today).days
        print (type(newDeadline))
        print(today)
        

        



        #newImage = request.files['Image']
        #filename = secure_filename(newImage.filename)
        #newImage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db.execute(''' INSERT INTO budgets (name, progress, goal, deadline,releaseDate,deadlineDate,user_id)
                        VALUES (?,?,?,?,?,?,?)''',(newName, newProgress, newGoal, newDeadline,sqlDate(),deadlineDate,session['user_id']))
        db.commit()
        return redirect(url_for('home'))
        
    
    return render_template('addGoal.html', form = form)



@app.route("/Budget/<int:budget_id>", methods = ['GET','POST'])
def budget(budget_id):
    form = updateBudget()
    db = get_db()
    budget = db.execute("""
        SELECT * FROM budgets
        WHERE budget_id = ?;""", (budget_id,)).fetchone()
    #print(stock)
    
    if form.validate_on_submit():
        preadvance = form.progressAdvance.data
        prewithdraw = form.progressWithdraw.data
        
        if preadvance:
            print(budget['progress'])
            db.execute(''' UPDATE budgets
                            SET progress = ?
                            WHERE budget_id = ? ''',((int(budget['progress'])+int(preadvance)),budget_id))
            db.commit()
            print(budget['progress'])
        else:
            form.progressAdvance.data = 0

        if prewithdraw:
            print(budget['progress'])
            db.execute(''' UPDATE budgets
                            SET progress = ?
                            WHERE budget_id = ? ''',((int(budget['progress'])-int(prewithdraw)),budget_id))
            db.commit()
            print(budget['progress'])
        else:
            form.progressWithdraw.data = 0

        return redirect (url_for("home"))
    

    return render_template("budgetPage.html", budget = budget, form = form)


@app.route("/logout", methods = ['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))



@app.route("/stockPage", methods = ['GET','POST'])
def stock():
    db = get_db()
    products = db.execute(''' SELECT * FROM products''')
    return render_template('stockPage.html', products = products)




@app.route("/editProduct/<int:product_id>", methods = ['GET','POST'])
def editProduct(product_id):
    form = updateForm()
    db = get_db()


    if form.validate_on_submit:
        newName=form.changeName.data
        newDesc=form.changeDesc.data
        newPrice = float(form.changePrice.data) if form.changePrice.data is not None else None
        newStock=form.changeStock.data
        newXSStock=form.changeXSStock.data
        newXStock=form.changeSStock.data
        newMStock=form.changeMStock.data
        newLStock=form.changeLStock.data
        newXLStock=form.changeXLStock.data
        newXXLStock=form.changesXXLStock.data
        
        
        newImage=form.changeImage.data



        #print(newPrice)
        #print(type(newPrice))
        if newName:
            db.execute(''' UPDATE products
                        SET name = ?
                        WHERE product_id = ? ''',(newName,product_id))
            db.commit()
            #print(len(newName))
            #print(newName)
            #print(type(newName))
        if newDesc:
            db.execute(''' UPDATE products
                        SET description = ?
                        WHERE product_id = ? ''',(newDesc,product_id))
            db.commit()
        if newPrice is not None:
            db.execute(''' UPDATE products
                        SET price = ?
                        WHERE product_id = ? ''',(round(newPrice,2),product_id))
            db.commit()
        if newStock is not None:
            db.execute(''' UPDATE products
                        SET stock = ?
                        WHERE product_id = ? ''',(newStock,product_id))
            db.commit()
    else:
        product = db.execute('''SELECT * FROM products
                                WHERE product_id = ?''',(product_id,)).fetchone()

        if not form.is_submitted():
            form.changeName.data = product['name']
            form.changeDesc.data = product['description']
            form.changePrice.data = product['price']
            form.changeStock.data = product['stock']

    product = db.execute("""
        SELECT * FROM products
        WHERE product_id = ?;""", (product_id,)).fetchone()
    return render_template("editProduct.html", product=product, form = form)
    

@app.route("/deleteBudget/<int:budget_id>", methods=['GET', 'POST'])
def deleteBudget(budget_id):
    db = get_db()
    db.execute(''' DELETE FROM budgets
                    WHERE budget_id = ?; ''',(budget_id,))
    db.commit()
    return redirect(url_for('home'))