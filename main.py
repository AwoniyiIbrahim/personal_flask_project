from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap5
import time
import json

app = Flask(__name__)
app.secret_key = '8df7426rh5i4hf9x'
bootstrap = Bootstrap5(app)
date = time.strftime('%Y')


# Form
class Contact_class(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(message='You must type a valid email (with "@" and ".")')])
    phone = StringField('Phone number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    contact_info = Contact_class()
    msg_sent = False
    if contact_info.validate_on_submit():
        message={
            "name":contact_info.name.data,
            "email":contact_info.email.data,
            "phone":contact_info.phone.data,
            "message":contact_info.message.data
            }
        try:
            with open("test.json",'r') as json_file:
                json_data=json.load(json_file)
        except (FileNotFoundError,json.JSONDecodeError):
            with open("test.json","w") as json_file:
                json_data=[]
        json_data.append(message)
        with open("test.json", "w") as json_file:
         json.dump(json_data,json_file,indent=4)
        msg_sent = True
        contact_info = Contact_class(formdata=None)
    return render_template('contact.html', form=contact_info, msg_sent=msg_sent)

@app.route('/projects')
def project():
    return render_template('projects.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.context_processor
def footer():
    return {'year': date}

if __name__ == '__main__':
    app.run(debug=True, port=5007)
