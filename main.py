from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask import Response

from data import create_app, create_database, read_match_result
from mail import Match, format_email, send_email

db = SQLAlchemy()
app = create_app(db)
create_database(app, db)
mail_handler = Mail(app)

@app.route('/')
def home():
    return "<h1>Hello World</h1>"

# POST localhost:5000/api/signup
@app.route('/api/signup', methods=['POST'])
def signup():
    # email = request.form.get('email')
    # gender = request.form.get('gender')
    # if gender == "male"
    # elif gender == "female"
    # elif gender == "..."
    pass

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


class User(db.Model):
    email = db.Column(db.String(150), primary_key=True)
    name = db.Column(db.String(150))
    race = db.Column(db.String(150))
    preferred_race = db.Column(db.String(150))
    q1 = db.Column(db.String(500))
    q2 = db.Column(db.String(500))
    q3 = db.Column(db.String(500))
    # q4
    # q5


# will run the web server only when we are in the main file (prevent from running it when main is imported by another file)
if __name__ == '__main__':
    # easiest way to run a flask app -- start a web server
    # every time we make a change to the python code, it will rerun the web server
    app.run(debug=True)
