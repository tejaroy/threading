from flask import *
from flask_sqlalchemy import *
from flask_migrate import *
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///teja1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Profile(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first_name=db.Column(db.String(20),unique=False,nullable=False)
    last_name=db.Column(db.String(20),unique=False,nullable=False)
    username = db.Column(db.String(25), unique=False,nullable=False)
    age=db.Column(db.Integer,nullable=False)
    phonenumber = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"first_name:{self.first_name},last_name:{self.last_name},username:{self.username},Age:{self.age},phonenumber:{self.phonenumber}"



@app.route('/')
def index():
    profiles=Profile.query.all()
    return render_template('index.html',profiles=profiles)

@app.route('/add_data')
def add_profile():
    return render_template('add_profile.html')



@app.route('/add',methods=['POST'])
def profile():
    first_name=request.form.get("first_name")
    last_name=request.form.get("last_name")
    username = request.form.get('username')
    age=request.form.get("age")
    phonenumber = request.form.get('phonenumber')

    if first_name != " " and last_name != " " and username != " " and age is not None and phonenumber is not None:
        p = Profile(first_name=first_name, last_name=last_name, username=username, age=age, phonenumber=phonenumber)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/delete/<int:id>')
def erase(id):

    data=Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


@app.route('/add_data/<int:id>/update', methods=['GET','POST'])
def update(id):
    data=Profile.query.filter_by(id=id).first()
    print(request.method)
    if request.method == 'POST':

        if data:
            data.first_name = request.form.get("first_name")
            data.last_name = request.form.get("last_name")
            data.username = request.form.get('username')
            data.age = request.form.get("age")
            data.phonenumber = request.form.get('phonenumber')
            db.session.commit()
            return redirect(f'/')
        return f"PROFILE with id = {id} Does not exist"

    return render_template('add_profile1.html', data=data)


if __name__=='__main__':
    app.run(debug=True)