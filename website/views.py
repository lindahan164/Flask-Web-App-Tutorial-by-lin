from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        status =request.form.get('Status')
        contact =request.form.get('contact')
        company_name= request.form.get('SCompanyName')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id ,Status=status ,SCompanyName=company_name , contact=contact)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



@views.route('/Board', methods=['GET', 'POST'])
def Board():
    notedb = Note.query.filter_by(id=Note.data).first()
    return render_template("Board.html", user=current_user)


@views.route('/notes')
def notes():
    notes = Note.query.all()
    return render_template('notes.html', notes=notes)