from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    check_in = db.Column(db.String(10), nullable=False)
    check_out = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Guest {self.name} {self.surname}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    guests = Guest.query.all()
    return render_template('index.html', guests=guests)

@app.route('/add_guest', methods=['GET', 'POST'])
def add_guest():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        
        new_guest = Guest(name=name, surname=surname, check_in=check_in, check_out=check_out)
        db.session.add(new_guest)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_guest.html')

@app.route('/delete_guest/<int:guest_id>')
def delete_guest(guest_id):
    guest = Guest.query.get(guest_id)
    db.session.delete(guest)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)