from flask import Flask, render_template, request, redirect, url_for
import random
import json
import os
import uuid

app = Flask(__name__)

data_file = 'people.json'

# JSON 데이터 불러오기
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# JSON 데이터 저장
def save_data(data):
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 팀 구성 함수 (최대 5명까지)
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
    people = load_data()
    return render_template('form.html', people=people)

@app.route('/add', methods=['POST'])
def add():
    people = load_data()
    new_person = {
        'id': str(uuid.uuid4()),  # 고유 ID 생성
        'name': request.form['name'],
        'gender': request.form['gender'],
        'age': request.form['age'],
        'car': 'car' in request.form
    }
    people.append(new_person)
    save_data(people)
    return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    people = load_data()
    people = [p for p in people if p['id'] != id]
    save_data(people)
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    people = load_data()
    person = next((p for p in people if p['id'] == id), None)
    if not person:
        return redirect(url_for('index'))

    if request.method == 'POST':
        person['gender'] = request.form['gender']
        person['age'] = request.form['age']
        person['car'] = 'car' in request.form
        save_data(people)
        return redirect(url_for('index'))

    return render_template('edit.html', person=person)

@app.route('/pair')
def pair():
    people = load_data()
    male_group = [p for p in people if p['gender'] == 'male']
    female_group = [p for p in people if p['gender'] == 'female']

    male_teams = make_pairs(male_group)
    female_teams = make_pairs(female_group)

    return render_template('result.html', male_teams=male_teams, female_teams=female_teams)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render 환경 대응
    app.run(host='0.0.0.0', port=port)
