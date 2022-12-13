from api import app, multi_auth, request, jsonify, db
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.schemas.note import note_schema, notes_schema, NoteSchema, NoteRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from marshmallow import fields


@app.route("/notes/<int:note_id>", methods=["GET"])
@multi_auth.login_required
@doc(summary='Get note by id', description="Get note by id if it is public or authorized user's private", tags=['Notes'])
@doc(responses={"401": {"description": "Unauthorized"}})
@doc(responses={"404": {"description": "Not found"}})
@doc(responses={"403": {"description": "Forbidden"}})
@doc(security=[{"basicAuth": []}])
@marshal_with(NoteSchema, code=200)
def get_note_by_id(note_id):
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id == user.id) | (NoteModel.private == False))
    if note in notes:
        return note, 200
    return "Not your note!", 403
    # if note.author_id == user.id or not note.private:
    #     return note_schema.dump(note), 200
    # return f"Note is private", 403


@app.route("/notes", methods=["GET"])
@multi_auth.login_required
@doc(summary="Get all public and registered user's private notes", tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@doc(security=[{"basicAuth": []}])
def get_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.join(NoteModel.author).filter((UserModel.id == user.id) | (NoteModel.private == False))
    return notes, 200


@app.route("/notes", methods=["POST"])
@multi_auth.login_required
@doc(summary='Create note', tags=['Notes'])
@marshal_with(NoteSchema, code=201)
@use_kwargs(NoteRequestSchema, location="json")
@doc(security=[{"basicAuth": []}])
def create_note(**kwargs):
    user = multi_auth.current_user()
    note = NoteModel(author_id=user.id, **kwargs)
    # note = NoteModel(author_id=user.id, **note_data)
    note.save()
    return note, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
@doc(summary='Change note', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@use_kwargs({'text': fields.Str(), 'private': fields.Bool()}, location="json")
@doc(security=[{"basicAuth": []}])
def edit_note(note_id, **kwargs):
    author = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    note_data = {**kwargs}
    if note.author_id == author.id:
        note.text = note_data["text"]
        note.private = note_data.get("private") or note.private
        note.save()
        return note, 200
    else:
        return f"Forbidden", 403


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
@doc(summary='Delete note', tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@doc(security=[{"basicAuth": []}])
def delete_note(note_id):
    author = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    if note.author_id == author.id:
        note.delete()
        return f"Note {note_id} deleted", 200
    return f"Forbidden", 403


@app.route("/notes/<int:note_id>/tags", methods=["PUT"])
@doc(summary="Set tags to Note", tags=['Notes'])
@use_kwargs({"tags_id": fields.List(fields.Int())}, location='json')
@marshal_with(NoteSchema)
def note_add_tags(note_id, **kwargs):
    note = get_object_or_404(NoteModel, note_id)
    tags_id = kwargs["tags_id"]
    for tag_id in tags_id:
        tag = get_object_or_404(TagModel, tag_id)
        note.tags.append(tag)
    db.session.commit()
    return note, 200


@app.route("/notes/archive/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
@doc(summary="Restore note from archive", tags=['Notes'])
@marshal_with(NoteSchema, code=200)
@doc(security=[{"basicAuth": []}])
def restore_note(note_id):
    note = get_object_or_404(NoteModel, note_id)
    user = multi_auth.current_user()
    if user.id == note.author_id:
        note.restore()
        return note, 200
    else:
        return f"Forbidden", 403

# TODO доделать!


@app.route("/notes/archive")
@multi_auth.login_required
@doc(summary="Show archive notes", tags=['Notes'])
@marshal_with(NoteSchema(many=True), code=200)
@doc(security=[{"basicAuth": []}])
def get_archive_notes():
    user = multi_auth.current_user()
    notes = NoteModel.query.filter((NoteModel.archive == True) & (NoteModel.author_id == user.id))
    return notes, 200
