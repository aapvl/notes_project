from api import app, docs
from config import Config
from api.handlers import auth, note, user, tag
import commands

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE

# Users docs
docs.register(user.get_user_by_id)
docs.register(user.get_users)
docs.register(user.create_user)
docs.register(user.edit_user)
docs.register(user.delete_user)
# Notes docs
docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.edit_note)
docs.register(note.delete_note)
docs.register(note.note_add_tags)
# Tags docs
docs.register(tag.get_all_tags)
docs.register(tag.get_tag_by_id)
docs.register(tag.create_tag)
docs.register(tag.delete_tag)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
