from flask import Flask, render_template, request
import random

app = Flask(__name__)

class Person:
    def __init__(self, name, gender, age_group, has_car):
        self.name = name
        self.gender = gender
        self.age_group = age_group  # 'young' or 'old'
        self.has_car = has_car      # True or False

    def __repr__(self):
        return f"{self.name} ({self.gender}, {self.age_group}, {'car' if self.has_car else 'no car'})"

def group_and_pair(people):
    young = [p for p in people if p.age_group == 'young']
    old = [p for p in people if p.age_group == 'old']
    random.shuffle(young)
    random.shuffle(old)
    pairs = []
    while young and old:
        pairs.append((young.pop(), old.pop()))
    remaining = young + old
    while len(remaining) >= 2:
        pairs.append((remaining.pop(), remaining.pop()))
    if remaining:
        pairs.append((remaining[0],))  # 1명 남을 경우
    return pairs

def assign_teams(male_pairs, female_pairs):
    all_pairs = male_pairs + female_pairs
    random.shuffle(all_pairs)
    teams = []
    team = []

    for pair in all_pairs:
        team.extend(pair)
        if len(team) == 6:
            if len(all_pairs) == 1 and len(pair) == 1:
                continue
            teams.append(team)
            team = []
    if team:
        teams.append(team)
    return teams

def ensure_car_owners(teams):
    for team in teams:
        car_owners = [p for p in team if p.has_car]
        if len(car_owners) < 1:
            for person in team:
                person.has_car = True
                break
    return teams

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        people = []
        for i in range(len(request.form.getlist('name'))):
            name = request.form.getlist('name')[i]
            gender = request.form.getlist('gender')[i]
            age_group = request.form.getlist('age_group')[i]
            has_car = request.form.getlist('has_car')[i] == 'yes'
            people.append(Person(name, gender, age_group, has_car))

        male = [p for p in people if p.gender == 'male']
        female = [p for p in people if p.gender == 'female']

        male_pairs = group_and_pair(male)
        female_pairs = group_and_pair(female)
        teams = assign_teams(male_pairs, female_pairs)
        teams = ensure_car_owners(teams)

        return render_template('result.html', teams=teams)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
