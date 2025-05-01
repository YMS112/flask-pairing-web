from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 모델 정의
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    car = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Person {self.name}>"

# DB 초기화 (한 번만 실행하거나 따로 관리)
with app.app_context():
    db.create_all()

# 팀 구성 함수
def make_pairs(group):
    random.shuffle(group)
    teams = []
    while len(group) >= 4:
        team = []
        while len(team) < 4 and group:
            team.append(group.pop())
        teams.append(team)
    if group:
        if teams and len(teams[-1]) + len(group) <= 5:
            teams[-1].extend(group)
        else:
            teams.append(group)
    return teams

@app.route('/')
def index():
    people = Person.query.all()
    return render_template('form.html', people=people)

@app.route('/add', methods=['POST'])
def add():
    new_person = Person(
        name=request.form['name'],
        gender=request.form['gender'],
        age=request.form['age'],
        car='car' in request.form
    )
    db.session.add(new_person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    person = Person.query.get_or_404(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    person = Person.query.get_or_404(id)
    if request.method == 'POST':
        person.gender = request.form['gender']
        person.age = request.form['age']
        person.car = 'car' in request.form
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', person=person)

@app.route('/pair')
def pair():
    male_group = Person.query.filter_by(gender='male').all()
    female_group = Person.query.filter_by(gender='female').all()

    male_teams = make_pairs(male_group)
    female_teams = make_pairs(female_group)

    return render_template('result.html', male_teams=male_teams, female_teams=female_teams)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Render에서 PORT 환경변수를 사용
    app.run(host='0.0.0.0', port=port)
