# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, WeatherForm, RegistrationForm
import requests, smtplib
from bs4 import BeautifulSoup as bs
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/w', methods=['POST'])
@login_required
def w():
#    form = WeatherForm()
#    user = User.query.filter_by(username=form.username.data).first()
    fromaddr = 'mg.test.robot@gmail.com'
    mypass = '27RoBot27'
    toaddr = "mgodkin@gmail.com"
#    toaddr = user.email

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
        rqst = requests.get('https://sinoptik.com.ru/погода-' + city)
        soup = bs(rqst.text, 'html.parser')

        p3 = soup.select('.temperature .p3')
        weather1 = p3[0].getText()

        p4 = soup.select('.temperature .p4')
        weather2 = p4[0].getText()

        p5 = soup.select('.temperature .p5')
        weather3 = p5[0].getText()

        p6 = soup.select('.temperature .p6')
        weather4 = p6[0].getText()

        p = soup.select('.rSide .description')
        weather = p[0].getText()

        f.write('----------------------------------' + '\n' +
                weather.strip() + '\n' +
                'Утром: ' + weather1 + ' ' + weather2 + '\n' +
                'Вечером: ' + weather3 + ' ' + weather4 + '\n')

    pw = soup.select('.oDescription .rSide .description')
    people_weather = pw[0].getText()

    f.write('----------------------------------' + '\n' +
            '\n' + people_weather.strip() + '\n' + '\n' +
            '----------------------------------' + '\n' + '\n' +
            'Хорошего всем настроения! Ваш робот.' + '\n')

    f.close()

    with open('weather.txt', 'r') as f:
        msg_body = f.read()

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 'Привет от погодного робота'

    msg.attach(MIMEText(str(msg_body), 'plain'))

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
    form = WeatherForm()
    return render_template('weather.html', title='Рассылка погоды', form=form)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)