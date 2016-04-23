# -*- coding: utf-8
from flask import Flask, render_template, request, redirect, session
from uuid import uuid4
from werkzeug.debug import DebuggedApplication
import json

app = Flask(__name__)
app.secret_key = 'R^^$(200xxaWA0*!~'

app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
notes = [{'uid': 0, 'title': "Tytul", 'content': "Tresc pierwszej notatki"},
         {'uid': 1, 'title': '2', 'content': 'Tresc drugiej notki'},
         {'uid': 2, 'title': '3', 'content': 'Tresc trzeciej'}]
current_uid = 1


@app.route('/', methods=['POST', 'GET'])
def index():
    global current_uid
    if request.method == 'GET':
        return json.dumps(notes)
    if request.method == 'POST':
        print "-------------------------------------------------"
        print request.data
        try:
            note = json.loads(request.data)
            if 'title' not in note or 'content' not in note:
                return u'Brak pola "title" i/lub "content"', 400
            note.update({'uid': current_uid})
            notes.append(note)
            current_uid += 1
        except ValueError, e:
            return u'Oczekuję formatu JSON', 400
        return json.dumps(notes), 201


@app.route('/<uid>', methods=['PUT', 'GET', 'DELETE'])
def note(uid):
    requested_note = None
    index = 0
    for note in notes:
        if note['uid'] == int(uid):
            requested_note = note
        else:
            index += 1
    if request.method == 'GET':
        if requested_note != None:
            return json.dumps(requested_note)
        return "Nie znaleziono notatki", 404
    if request.method == 'PUT':
        print request.data
        if requested_note != None:
            requested_note.update(json.loads(request.data))
            return json.dumps(requested_note), 201
        return "Nie znaleziono notatki", 404
    if request.method == 'DELETE':
        if requested_note != None:
            notes.remove(requested_note)
            return u"Usunięto" + '\n'
        return "Nie znaleziono notatki", 404


if __name__ == '__main__':
    app.run()
