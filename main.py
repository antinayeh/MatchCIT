from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Response

from flask import Blueprint, render_template, request, flash, redirect, url_for

from data import create_app, create_database, read_match_result
from mail import Match, format_email, send_email

db = SQLAlchemy()
app = create_app(db)

class User(db.Model):
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), primary_key=True)
    gender = db.Column(db.String(150))
    sex_or = db.Column(db.String(150))

    age = db.Column(db.Integer)
    preferred_age = db.Column(db.Integer)
    height = db.Column(db.Float)
    preferred_height = db.Column(db.Float)

    race = db.Column(db.String(150))
    preferred_race = db.Column(db.String(150))

    religion = db.Column(db.String(150))
    mbti = db.Column(db.String(150))
    
    aesthetic = db.Column(db.String(150))
    #hobbies 
    swimming = db.Column(db.Integer)
    cooking_baking = db.Column(db.Integer) 
    singing = db.Column(db.Integer)
    reading = db.Column(db.Integer)
    video_game = db.Column(db.Integer)
    tv = db.Column(db.Integer)
    outdoor = db.Column(db.Integer)
    art = db.Column(db.Integer)
    traveling = db.Column(db.Integer)
    music = db.Column(db.Integer)

    #love languages
    service = db.Column(db.Integer)
    time = db.Column(db.Integer) 
    touch = db.Column(db.Integer)
    gift = db.Column(db.Integer)
    affirmation = db.Column(db.Integer)


    def __str__(self) -> str:
        attributes = [self.email, self.name, self.gender, self.sex_or, str(self.age), 
            str(self.preferred_age), str(self.height), str(self.preferred_height), 
            self.race, self.preferred_race, self.aesthetic, self.mbti, self.religion,
            str(self.swimming), str(self.cooking_baking), str(self.singing), 
            str(self.reading), str(self.video_game), 
            str(self.tv), str(self.outdoor), str(self.art), str(self.traveling), 
            str(self.music), 
            str(self.service), str(self.time), str(self.touch), str(self.gift), str(self.affirmation)]
        return "\n".join(attributes)

create_database(app, db)
mail_handler = Mail(app)

@app.route('/')
def home():
    return "<h1>Hello World</h1>"

# POST localhost:5000/api/signup
@app.route('/api/signup', methods=['POST'])
def signup():
    print(f'request.form: {request.form}')

    # ([('name', 'a'), ('email', 'a'), ('age', '20'), ('ft', '6'), ('inch', '2'),
    #  ('gender', 'Non-binary'), ('sexualorient', 'Non-binary'), ('race', 'Native Hawaiian and Other Pacific Islander'),
    #   ('preferred-age', '20'), ('preferred-ft', '5'), ('preferred-inch', '5'), ('preferred-race', 'Native Hawaiian and Other Pacific Islander'),
    #    ('religion', 'None'), ('mbti', 'estp'), ('hobby5', 'on'), ('hobby9', 'on'), ('aesthetic', 'on'), ('lovelanguage1', '3'), 
    #    ('lovelanguage2', '3'), ('lovelanguage3', '3'), ('lovelanguage4', '3'), ('lovelanguage5', '3')])
    email = request.form.get('email')
    name = request.form.get('name')
    gender = request.form.get('gender')
    sex_or = request.form.get('sexualorient')

    age = int(request.form.get('age'))
    preferred_age = int(request.form.get('preferred-age'))

    height_feet = int(request.form.get('ft'))
    height_inches = int(request.form.get('inch'))
    height_in_inches = 12 * height_feet + height_inches

    preferred_height_feet = int(request.form.get('preferred-ft'))
    preferred_height_inches = int(request.form.get('preferred-inch'))
    preferred_height_in_inches = 12 * preferred_height_feet + preferred_height_inches 

    race = request.form.get('race')
    preferred_race = request.form.get('preferred-race')


    #aesthetic 
    if request.form.get('aesthetic-fc'):
        aesthetic = 'Feminine Charm'
    elif request.form.get('aesthetic-fl'):
        aesthetic = 'Fresh Lavender'

    elif request.form.get('aesthetic-r'):
        aesthetic = 'Rustic Feels'
    
    elif request.form.get('aesthetic-m'):
        aesthetic = 'The Minimalist'
    else:
        aesthetic = None

    

    # #hobbies 

    if request.form.get('hobby1'):
        swimming = 1
    else:
        swimming = 0

    if request.form.get('hobby2'):
        cooking_baking = 1
    else:
        cooking_baking = 0

    if request.form.get('hobby3'):
        singing = 1
    else:
        singing = 0
    
    if request.form.get('hobby4'):
        video_game = 1
    else:
        video_game = 0

    if request.form.get('hobby5'):
        tv = 1
    else:
        tv = 0

    if request.form.get('hobby6'):
        reading = 1
    else:
        reading = 0

    if request.form.get('hobby7'):
        outdoor = 1
    else:
        outdoor = 0

    if request.form.get('hobby8'):
        art = 1
    else:
        art = 0

    if request.form.get('hobby9'):
        traveling = 1
    else:
        traveling = 0

    if request.form.get('hobby10'):
        music = 1
    else:
        music = 0


    mbti = request.form.get('mbti')

    religion = request.form.get('religion')

    # #love languages
    service = int(request.form.get('lovelanguage1'))
    time = int(request.form.get('lovelanguage2'))
    touch = int(request.form.get('lovelanguage3'))
    gift = int(request.form.get('lovelanguage4'))
    affirmation = int(request.form.get('lovelanguage5'))

    new_user = User(email = email, name = name, gender = gender, sex_or = sex_or, age = age, preferred_age = preferred_age, 
        height = height_in_inches, preferred_height = preferred_height_in_inches, race = race, preferred_race = preferred_race, aesthetic = aesthetic,
        mbti = mbti, religion = religion, swimming = swimming, cooking_baking = cooking_baking, singing = singing, reading = reading, 
        video_game = video_game, tv = tv, outdoor = outdoor, art = art, traveling = traveling, music = music, service = service, 
        time = time, touch = touch, gift = gift, affirmation = affirmation)

    print(new_user)
    db.session.add(new_user)
    db.session.commit()

    # if gender == "male"
    # elif gender == "female"
    # elif gender == "..."
    return render_template('matches.html')

# GET localhost:5000/api/notify
@app.route('/api/notify')
def notify():
    # read match results from a csv file and send email notifications
    df = read_match_result()
    app.logger.debug(df.head(5))
    # df.apply(lambda row: send_email(app, mail_handler, row['email'], format_email(row['name'], [
    #     Match(row['match1_name'], row['match1_email']),
    #     Match(row['match2_name'], row['match2_email']),
    #     Match(row['match3_name'], row['match3_email']),
    # ])), axis=1)

    for index, row in df.iterrows():
        name = row['name']
        email = row['email']
        match1 = Match(row['match1_name'], row['match1_email'])
        match2 = Match(row['match2_name'], row['match2_email'])
        match3 = Match(row['match3_name'], row['match3_email'])
        email_content = format_email(name, [match1, match2, match3])
        send_email(app, mail_handler, email, email_content)

    return Response(status=200)






# will run the web server only when we are in the main file (prevent from running it when main is imported by another file)
if __name__ == '__main__':
    # easiest way to run a flask app -- start a web server
    # every time we make a change to the python code, it will rerun the web server
    app.run(debug=True)
