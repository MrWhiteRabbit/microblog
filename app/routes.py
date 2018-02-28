# -*- coding: utf-8 -*-
from flask import render_template
from app import app

import requests, bs4, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Max'}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/weather')
def weather():
    user = {'username': 'Max'}
#    fromaddr = "mg.test.robot@gmail.com"
#    mypass = "27RoBot27"
#    toaddr = "mgodkin@gmail.com"

#    city_arr = [
#        'москва',
#        'ставрополь',
#        'ростов-на-дону',
#        'иву'
#    ]

#    f = open('weather.txt', 'w')
#    f.write('Привет, Семья! Вот прогноз погоды в наших городах на сегодня:' + '\n' + '\n')

#    for el in range(0, len(city_arr)):
#        city = city_arr[el]
#    city = 'москва'
    s = requests.get('https://sinoptik.com.ru/погода-москва')
#    b = bs4.BeautifulSoup(s.text, 'html.parser')

#    p3 = b.select('.temperature .p3')
#    pogoda1 = p3[0].getText()

#    p4 = b.select('.temperature .p4')
#    pogoda2 = p4[0].getText()

#    p5 = b.select('.temperature .p5')
#    pogoda3 = p5[0].getText()

#    p6 = b.select('.temperature .p6')
#    pogoda4 = p6[0].getText()

#    p = b.select('.rSide .description')
#    pogoda = p[0].getText()
#    pogoda_show = {pogoda.strip()}
#        f.write('----------------------------------' + '\n' +
#               pogoda.strip() + '\n' +
#                'Утром: ' + pogoda1 + ' ' + pogoda2 + '\n' +
#                'Вечером: ' + pogoda3 + ' ' + pogoda4 + '\n')

#    np = b.select('.oDescription .rSide .description')
#    nar_pogoda = np[0].getText()

#    f.write('----------------------------------' + '\n' +
#            '\n' + nar_pogoda.strip() + '\n' + '\n' +
#            '----------------------------------' + '\n' + '\n' +
#            'Хорошего всем настроения! Ваш робот.' + '\n')

#    f.close()

#    print('Прогноз погоды сформирован в файл.')

#    f = open('weather.txt', 'r')

#l = f.read()

#    f.close()

#    msg = MIMEMultipart()
#    msg['From'] = fromaddr
#    msg['To'] = toaddr
#    msg['Subject'] = 'Привет от погодного робота'
#
#    msg.attach(MIMEText(str(l), 'plain'))
#
#    server = smtplib.SMTP('smtp.gmail.com', 587)
#    server.starttls()
#    server.login(fromaddr, mypass)
#    text = msg.as_string()
#    server.sendmail(fromaddr, toaddr, text)
#    server.quit()

#    print('Письмо с прогнозом отправлено.')
    return render_template('weather.html', title='Рассылка погоды', user=user)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)