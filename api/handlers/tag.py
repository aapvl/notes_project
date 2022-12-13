from api import app, request, multi_auth, jsonify, db
from api.models.tag import TagModel
from api.schemas.tag import tag_schema, tags_schema, TagSchema, TagRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from sqlalchemy.exc import IntegrityError
from marshmallow import fields


@app.route("/tags")
@doc(summary='Get all tags.', tags=['Tags'])
@marshal_with(TagSchema(many=True), 200)
def get_all_tags():
    tags = TagModel.query.all()
    return tags, 200


@app.route("/tags/<int:tag_id>")
@doc(summary='Get tag by id.', tags=['Tags'])
@marshal_with(TagSchema, 200)
def get_tag_by_id(tag_id):
    tag = get_object_or_404(TagModel, tag_id)
    return tag, 200


@app.route("/tags", methods=["POST"])
@doc(summary='Create new tag', tags=['Tags'])
@marshal_with(TagSchema, code=201)
@use_kwargs(TagRequestSchema, location='json')
def create_tag(**kwargs):
    tag = TagModel(**kwargs)
    try:
        tag.save()
    except IntegrityError:
        return "tag name must be unique", 400
    return tag, 201


@app.route("/tags/<int:tag_id>", methods=["DELETE"])
@doc(summary="Delete tag by id", tags=["Tags"])
def delete_tag(tag_id):
    tag = TagModel.query.get(tag_id)
    if tag is not None:
        tag.delete()
    return f"Tag {tag_id} deleted", 200


# TODO добавить PUT обработчик
