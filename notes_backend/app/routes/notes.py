from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields, validate, EXCLUDE
from ..storage import list_notes, get_note, create_note, update_note, delete_note

blp = Blueprint(
    "Notes",
    __name__,
    url_prefix="/notes",
    description="CRUD endpoints for managing notes"
)


class NoteSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(dump_only=True, description="Unique note identifier")
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200), description="Title of the note")
    content = fields.Str(required=True, validate=validate.Length(min=1), description="Content of the note")
    created_at = fields.Str(dump_only=True, description="ISO timestamp when the note was created")
    updated_at = fields.Str(dump_only=True, description="ISO timestamp when the note was last updated")


class NoteUpdateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    title = fields.Str(validate=validate.Length(min=1, max=200), description="New title of the note")
    content = fields.Str(validate=validate.Length(min=1), description="New content of the note")


@blp.route("/")
class NotesList(MethodView):
    @blp.response(200, NoteSchema(many=True), description="List all notes")
    def get(self):
        """List all notes."""
        return list_notes()

    @blp.arguments(NoteSchema, as_kwargs=True)
    @blp.response(201, NoteSchema, description="Note created")
    def post(self, title, content):
        """Create a note with title and content."""
        note = create_note(title=title, content=content)
        return note


@blp.route("/<int:note_id>")
class NotesDetail(MethodView):
    @blp.response(200, NoteSchema, description="Get note by id")
    def get(self, note_id: int):
        """Get a single note by id."""
        note = get_note(note_id)
        if not note:
            abort(404, message="Note not found")
        return note

    @blp.arguments(NoteUpdateSchema, as_kwargs=True)
    @blp.response(200, NoteSchema, description="Updated note")
    def put(self, args, note_id: int, **kwargs):
        """
        Update an existing note by id.
        At least one of title or content must be provided.
        """
        # Because flask-smorest arguments with as_kwargs would pass fields directly;
        # however using method signature with args can be tricky. Normalize:
        payload = {}
        if isinstance(args, dict):
            payload = args
        else:
            payload = kwargs

        title = payload.get("title", None)
        content = payload.get("content", None)

        if title is None and content is None:
            abort(400, message="At least one of 'title' or 'content' must be provided")

        note = update_note(note_id, title=title, content=content)
        if not note:
            abort(404, message="Note not found")
        return note

    @blp.response(204, description="Note deleted")
    def delete(self, note_id: int):
        """Delete a note by id."""
        deleted = delete_note(note_id)
        if not deleted:
            abort(404, message="Note not found")
        return ""
