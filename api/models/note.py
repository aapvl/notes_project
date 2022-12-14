from api import db
from api.models.user import UserModel
from api.models.tag import TagModel

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('note_model_id', db.Integer, db.ForeignKey('note_model.id'), primary_key=True)
                )


class NoteModel(db.Model):
    # __name = "Author"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(UserModel.id))
    text = db.Column(db.String(255), unique=False, nullable=False)
    private = db.Column(db.Boolean(), default=True, nullable=False)
    tags = db.relationship(TagModel, secondary=tags, lazy='subquery', backref=db.backref('notes', lazy=True))
    archive = db.Column(db.Boolean(), unique=False, default=False, server_default='false')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        self.archive = True
        db.session.commit()

    def restore(self):
        self.archive = False
        db.session.commit()
