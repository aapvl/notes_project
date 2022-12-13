from api import app, request, multi_auth, jsonify
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/users/<int:user_id>")
@doc(summary='Get user by id.', tags=['Users'])
@marshal_with(UserSchema, code=200)
def get_user_by_id(user_id):
    user = get_object_or_404(UserModel, user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return user, 200


@app.route("/users")
@doc(summary='Get all users.', tags=['Users'])
@marshal_with(UserSchema(many=True), code=200)
def get_users():
    users = UserModel.query.all()
    return users, 200


@app.route("/users", methods=["POST"])
@doc(summary='Create user', tags=['Users'])
@marshal_with(UserSchema, code=201)
@use_kwargs(UserRequestSchema, location="json")
def create_user(**kwargs):
    # user_data = request.json
    user = UserModel(**kwargs)
    # TODO: добавить обработчик на создание пользователя с неуникальным username
    user.save()
    return user_schema.dump(user), 201


@app.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth.login_required(role="admin")
@doc(summary='Change username', tags=["Users"])
@marshal_with(UserSchema, code=200)
@use_kwargs(UserRequestSchema, location='json')
@doc(security=[{"basicAuth": []}])
def edit_user(user_id, **kwargs):
    user_data = UserModel(**kwargs)
    user = get_object_or_404(UserModel, user_id)
    user.username = user_data.username
    user.save()
    return user, 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth.login_required(role="admin")
@doc(summary='Delete user', tags=['Users'])
def delete_user(user_id):
    """
    Пользователь может удалять ТОЛЬКО свои заметки
    """
    raise NotImplemented("Метод не реализован")