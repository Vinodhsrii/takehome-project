import os
from flask import Flask,json, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@db:5432/groundspeed_devops'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route('/healthcheck')
def health_check():
    return json.dumps({'status': 'OK'})

@app.route('/message', methods = ['POST'])
def message_post():
    r_json = request.get_json()
    if 'message' in r_json:
        posted_message = r_json['message']
        message = Message(text=posted_message)
        db.session.add(message)
        db.session.commit()
        return json.dumps({'status': 'OK', 'message_id': message.id})
    return json.dumps({'status': 'FAIL', 'error': 'must include json in post with a "message" key'})

@app.route('/message/<message_id>', methods = ['GET'])
def message_get(message_id):
    try:
        message = db.session.query(Message).filter(Message.id == message_id).one()
        print(message)
        return json.dumps({'status': 'OK', 'message_text': message.text})
    except:
        return json.dumps({'status': 'FAIL', 'error': 'message_id({}) must exist'.format(message_id)})

if __name__ == '__main__':
    db.create_all()
    app.run('0.0.0.0', 80)