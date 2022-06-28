"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""
from py4web import action, request, abort, Field, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash

# le mie import per il FORM
from py4web.utils.form import Form, FormStyleDefault
from pydal.validators import IS_NOT_EMPTY

# le mie import per lo scraper
import requests
from bs4 import BeautifulSoup as bs
from random import randint
from time import *
from datetime import datetime
import xlsxwriter 

# app folder dei files
import os
from .settings import APP_FOLDER

import wikipedia

def my_scraper(URL, id):
    current_datetime = datetime.now().timestamp()
    str_current_datetime = str(current_datetime)

    LISTA_titoli = []
    LISTA_autori = []

    for page in range(1,2):

        formatUrl = (URL+str(page))

        req = requests.get(formatUrl)
        
        soup = bs(req.text, 'html.parser')

        titoli = soup.find_all('div', attrs={'class','titolo_release'})
        autori = soup.find_all('div', attrs={'class','nome_autore'})
        
        for fumetto in range(0, 24):
            print('Titolo \n' + titoli[fumetto].text)
            print('Autore ', autori[fumetto].text)
            LISTA_titoli.append(titoli[fumetto].text)
            LISTA_autori.append(autori[fumetto].text)
            sleep(randint(2,10))

    print(LISTA_titoli)

    file_name = str_current_datetime + '_' + 'la_mia_lista.xlsx'

    workbook = xlsxwriter.Workbook('apps/scraper/static/excel/' + file_name)
    worksheet = workbook.add_worksheet()

    for row_num, data in enumerate(LISTA_titoli):
        worksheet.write(row_num, 0, data)
    for row_num, data in enumerate(LISTA_autori):
        worksheet.write(row_num, 1, data)
    
    workbook.close()
    
    db.files_excel.insert(reference_file=id, file=file_name)

    print('File Excel generato con successo')

# controllers definition
@action("index", method=["GET", "POST"])
@action.uses('index.html', db)
def index(id=None):
    form = Form(db.siti_importati, id, deletable=False, formstyle=FormStyleDefault)
    welcome = "Benvenuto, per scaricare i file excel devi essere loggato."
    if form.accepted:
        URL = form.vars['website_url']
        id = form.vars['id']
        my_scraper(URL, id)
    if form.errors:
        redirect(URL('not_accepted'))

    return dict(form=form, welcome = welcome)


# controllers definition
@action("chisono")
@action.uses('chisono.html') 
def chisono():
    descrizione = 'Hi! My name is Giuseppe Giulio, I grew up in Barge in the woods of the western Alps. The bicycle was immediately the best way to explore the world around me. My first bike was the legendary aluminum frame "Vicini" with elastomer fork. I received it as a gift from my parents for the end of the fifth grade. That day I personally went to pick it up from the closest bike shop and I rode along the secondary roads of the plain to go home. Today I am passionate about the mountains in many ways: alpinism, sport climbing, bouldering and photography. I worked in the ICT consulting for many years and now I\'m 100% \focused on outdoor activities. I try to have a lifestyle in line with the concept of "Simple living". My guiding activity is focused on tours with small groups or individuals in remote places (mainly at high altitudes). I like to help the client to achieve his goals and I use coaching techniques.'
    return dict(descrizione=descrizione)


# controllers definition
@action("excel")
@action.uses('excel.html', db)
#@action.uses(auth.user)  
def excel():
    rows = db(db.siti_importati).select()
    rowsExcel = db(db.files_excel).select()

    return dict(rows=rows, rowsExcel=rowsExcel)
    

# controllers definition
@action("wiki")
@action.uses('wiki.html') 
def wiki():
    page = wikipedia.page('Web Scraping')
    search = wikipedia.search('pizza')
    pagetitle = page.title
    page = page.content
    return dict(search=search, pagTitle=pagetitle, pagContent=page)