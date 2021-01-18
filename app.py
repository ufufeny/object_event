from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)


class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Nickname = db.Column(db.String(45), nullable=True)
    Name = db.Column(db.String(45), nullable=True)
    Type = db.Column(db.String(45), nullable=True)
    Number = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Owner %r>' % self.id


class Rep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name_house = db.Column(db.String(45), nullable=True)
    Mark = db.Column(db.Integer, nullable=True)
    When = db.Column(db.Integer, nullable=True)
    Comment = db.Column(db.String(150), nullable=True)

    def __repr__(self):
        return '<Rep %r>' % self.id


class House(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=True)
    Name_owner = db.Column(db.String(45), nullable=True)
    Type = db.Column(db.String(45), nullable=True)
    Index = db.Column(db.String(45), nullable=True)
    Slots = db.Column(db.Integer, nullable=True)
    Status = db.Column(db.String(45), nullable=True)
    Data_open = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<House %r>' % self.id

    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(45), nullable=True)
    Name_house = db.Column(db.String(45), nullable=True)
    Type = db.Column(db.String(45), nullable=True)
    Data = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<Event %r>' % self.id


@app.route('/')
def index():
    house = House.query.order_by(House.id.desc()).all()
    return render_template('house.html',  house=house)


@app.route('/house')
def houses():
    events = Event.query.order_by(Event.id.desc()).all()
    house = House.query.order_by(House.id.desc()).all()

    return render_template('house.html', house=house, events=events)


@app.route('/house/<int:id>/rep')
def rep(id):
    house = House.query.order_by(House.id.desc()).all()
    rep = Rep.query.order_by(Rep.id.desc()).all()

    return render_template('rep.html', rep=rep, house=house)


@app.route('/house/<int:id>/rep/delete')
def rep_delete(id):

    rep = Rep.query.get(id)

    try:
        db.session.delete(rep)
        db.session.commit()
        return redirect('/house>')
    except:
        return "Не удалост удалить"


@app.route('/rep/<int:id>')
def rep_detail(id):
    house = House.query.get(id)
    try:
        rep = Rep.query.order_by(Rep.id.desc()).all()
        return render_template('rep.html', house=house, events=events, rep=rep)
    except:
        house = House.query.get(id)
        rep = Rep.query.order_by(Rep.id.desc()).all()
        return render_template('rep.html', house=house, houses=houses, rep=rep)


@app.route('/house/<int:id>')
def house_detail(id):
    house = House.query.get(id)
    houses = House.query.order_by(House.id.desc()).all()
    try:

        rep = Rep.query.order_by(Rep.id.desc()).all()
        event = Event.query.order_by(Event.id.desc()).all()
        events = Event.query.order_by(Event.id.desc()).all()
        return render_template('house_datail.html', house=house, houses=houses, event=event, events=events, rep=rep)
    except:
        event = Event.query.order_by(Event.id.desc()).all()
        rep = Rep.query.order_by(Rep.id.desc()).all()
        return render_template('house_datail.html', house=house, houses=houses, event=event, rep=rep)


#@app.route('/add_house', methods=['GET', 'POST'])
#def add_house():
#    if request.method == "POST":
#        Name = request.form['Name']
#        Type = request.form['Type']
#        Index = request.form['Index']
#        Slots = request.form['Slots']
#        Status = request.form['Status']
#        Name_owner = request.form['Name_owner']
#
#        house = House(Name=Name, Type=Type, Index=Index, Slots=Slots, Status=Status, Name_owner=Name_owner)
#
#        try:
#            db.session.add(house)
#            db.session.commit()
#            return redirect('/house')
#        except:
#            return "Не удалось добавить обьект"
#
#    else:
#        return render_template('add_house.html')


@app.route('/house/<int:id>/update', methods=['GET','POST'])
def house_update(id):
    house = House.query.get(id)
    event = Event.query.get(id)
    rep = Rep.query.get(id)
    if request.method == "POST":
        house.Name = request.form['Name']
        house.Type = request.form['Type']
        house.Index = request.form['Index']
        house.Slots = request.form['Slots']
        house.Status = request.form['Status']
        house.Data_open = request.form['Data_open']
        house.Name_owner = request.form['Name_owner']
        try:
            event.Name_house = request.form['Name']
        except:
            pass
        try:
            rep.Name_house = request.form['Name']
        except:
            pass

        try:
            db.session.commit()
            return redirect('/house')
        except:
            return "При редактировании произошла ошибка"
    else:
        rep = Rep.query.get(id)
        house = House.query.get(id)
        return render_template('house_update.html', house=house, rep=rep)


@app.route('/house/<int:id>/delete')
def house_delete(id):
    house = House.query.get_or_404(id)

    try:
        db.session.delete(house)
        db.session.commit()
        return redirect('/rep>')
    except:
        return "При удалении произошла ошибка"


@app.route('/house/<int:id>/add_event',  methods=['GET', 'POST'])
def house_add_event(id):
    house = House.query.get(id)
    if request.method == "POST":
        Name = request.form['Name']
        Type = request.form['Type']
        Name_house = request.form['Name_house']
        Data = request.form['Data']

        event = Event(Name=Name, Type=Type, Name_house=Name_house, Data=Data)

        try:
            db.session.add(event)
            db.session.commit()
            return redirect('/house')
        except:
            return "Не удалось добавить мероприятие"

    else:
        house = House.query.get(id)
        return render_template('add-event.html',house=house)


@app.route('/house/<int:id>/add_rep',  methods=['GET', 'POST'])
def house_add_rep(id):
    house = House.query.get(id)
    if request.method == "POST":
        Name_house = request.form['Name_house']
        Mark = request.form['mark']
        Comment = request.form['comment']
        When = request.form['When']

        rep = Rep(Mark=Mark, Comment=Comment, Name_house=Name_house, When=When)

        try:
            db.session.add(rep)
            db.session.commit()
            return redirect('/house')
        except:
            return "Не удалось добавить оценку"
    else:
        return render_template('add_rep.html', house=house)






@app.route('/posts')
def posts():
    owners = Owner.query.order_by(Owner.id.desc()).all()
    return render_template('posts.html', owners=owners)


@app.route('/posts/<int:id>/post')
def post(id):
    owner = Owner.query.get(id)
    house = House.query.order_by(House.id.desc()).all()
    owners = Owner.query.order_by(Owner.id.desc()).all()
    return render_template('post.html', owners=owners, house=house, owner=owner)


@app.route('/posts/<int:id>')
def post_detail(id):
    owner = Owner.query.get(id)
    house = House.query.get(id)
    houses = House.query.order_by(House.id.desc()).all()
    owners = Owner.query.order_by(Owner.id.desc()).all()
    return render_template('post_datail.html', owner=owner, house=house, houses=houses, owners=owners)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    owner = Owner.query.get_or_404(id)

    try:
        db.session.delete(owner)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"


@app.route('/posts/<int:id>/plus_event',  methods=['GET','POST'])
def post_plus_event(id):
    owner = Owner.query.get(id)
    house = House.query.order_by(House.id.desc()).all()
    if request.method == "POST":
        owner.house = request.form['house']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Не удалось добавить обьект"
    else:
        return render_template('plus_event.html', owner=owner, house=house)


@app.route('/posts/<int:id>/update', methods=['GET','POST'])
def post_update(id):
    owner = Owner.query.get(id)
    if request.method == "POST":
        owner.Name = request.form['Name']
        owner.Nickname = request.form['Nickname']
        owner.Type = request.form['Type']
        owner.Number = request.form['Number']


        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании произошла ошибка"
    else:
        owner = Owner.query.get(id)
        return render_template('post_update.html', owner=owner)


@app.route('/posts/<int:id>/add_house', methods=['GET', 'POST'])
def add_house(id):
    if request.method == "POST":
        Name = request.form['Name']
        Type = request.form['Type']
        Index = request.form['Index']
        Slots = request.form['Slots']
        Status = request.form['Status']
        Name_owner = request.form['Name_owner']
        Data_open = request.form['Data_open']

        house = House(Name=Name, Type=Type, Index=Index, Slots=Slots, Status=Status, Name_owner=Name_owner, Data_open=Data_open)

        try:
            db.session.add(house)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Не удалось добавить обьект"

    else:
        owner = Owner.query.order_by(Owner.id.desc()).all()
        return render_template('add_house.html',owner=owner)

@app.route('/create-owner', methods=['GET','POST'])
def create_owner():
    if request.method == "POST":
        Name = request.form['Name']
        Nickname = request.form['Nickname']
        Type = request.form['Type']
        Number = request.form['Number']

        owner = Owner(Name=Name, Nickname=Nickname, Type=Type, Number=Number)
        try:
            db.session.add(owner)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Не удалось отправить владельца"
    else:
        return render_template('create-owner.html')


@app.route('/events')
def events():
    event = Event.query.order_by(Event.id.desc()).all()
    return render_template('events.html', event=event)


#@app.route('/add-event', methods=['GET', 'POST'])
#def add_events():
#    if request.method == "POST":
#        Name = request.form['Name']
#        Type = request.form['Type']
#        Name_house = request.form['Name_house']
#
#        event = Event(Name=Name, Type=Type, Name_house=Name_house)
#
#        try:
#            db.session.add(event)
#            db.session.commit()
#            return redirect('/events')
#        except:
#            return "Не удалось добавить мероприятие"
#
#    else:
#        return render_template('add-event.html')


@app.route('/events/<int:id>')
def event_detail(id):
    event = Event.query.get(id)
    return render_template('event_datail.html', event=event)


@app.route('/events/<int:id>/delete')
def event_delete(id):
    event = Event.query.get_or_404(id)

    try:
        db.session.delete(event)
        db.session.commit()
        return redirect('/events')
    except:
        return "При удалении произошла ошибка"


@app.route('/events/<int:id>/update', methods=['GET','POST'])
def event_update(id):
    event = Event.query.get(id)
    if request.method == "POST":
        event.Name = request.form['Name']
        event.Type = request.form['Type']
        event.Data = request.form['Data']

        try:
            db.session.commit()
            return redirect('/events')
        except:
            return "При редактировании произошла ошибка"
    else:
        event = Event.query.get(id)
        return render_template('event_update.html', event=event)


if __name__ == "__main__":
    app.run(debug=True)