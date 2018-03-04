# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
import requests, bs4, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    #user = {'username': 'Max'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Hmmm... Its ok blog!'
        },
        {
            'author': {'username': 'Ипполит'},
            'body': 'Какая гадость эта ваша заливная рыба!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
          return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
       user = User.query.filter_by(username=form.username.data).first()
       if user is None or not user.check_password(form.password.data):
           flash('Неправильные Имя или Пароль!')
           return redirect(url_for('login'))
       login_user(user, remember=form.remember_me.data)
       next_page = request.args.get('next')
       if not next_page or url_parse(next_page).netloc != '':
           next_page = url_for('index')
       return redirect(url_for('index'))
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/w', methods=['POST'])
@login_required
def w():
    fromaddr = "mg.test.robot@gmail.com"
    mypass = "27RoBot27"
    toaddr = "mgodkin@gmail.com"

    city_arr = [
        'москва',
        'ставрополь',
        'ростов-на-дону',
        'иву'
    ]

    f = open('weather.txt', 'w')
    f.write('Привет, Семья! Вот прогноз погоды в наших городах на сегодня:' + '\n' + '\n')

    for el in range(0, len(city_arr)):
        city = city_arr[el]
        s = requests.get('https://sinoptik.com.ru/погода-' + city)
        b = bs4.BeautifulSoup(s.text, 'html.parser')

        p3 = b.select('.temperature .p3')
        pogoda1 = p3[0].getText()

        p4 = b.select('.temperature .p4')
        pogoda2 = p4[0].getText()

        p5 = b.select('.temperature .p5')
        pogoda3 = p5[0].getText()

        p6 = b.select('.temperature .p6')
        pogoda4 = p6[0].getText()

        p = b.select('.rSide .description')
        pogoda = p[0].getText()

        f.write('----------------------------------' + '\n' +
                pogoda.strip() + '\n' +
                'Утром: ' + pogoda1 + ' ' + pogoda2 + '\n' +
                'Вечером: ' + pogoda3 + ' ' + pogoda4 + '\n')

    np = b.select('.oDescription .rSide .description')
    nar_pogoda = np[0].getText()

    f.write('----------------------------------' + '\n' +
            '\n' + nar_pogoda.strip() + '\n' + '\n' +
            '----------------------------------' + '\n' + '\n' +
            'Хорошего всем настроения! Ваш робот.' + '\n')

    f.close()


    f = open('weather.txt', 'r')

    l = f.read()

    f.close()

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Привет от погодного робота'

    msg.attach(MIMEText(str(l), 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, mypass)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return redirect(url_for('index'))


@app.route('/weather', methods=['GET', 'POST'])
@login_required
def weather():
    user = {'username': 'Max'}
    form = LoginForm()
    return render_template('weather.html', title='Рассылка погоды', user=user, form=form)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)