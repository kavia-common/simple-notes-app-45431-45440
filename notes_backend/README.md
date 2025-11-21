# Simple Notes Backend (Flask)

A minimal RESTful API for creating, viewing, editing, and deleting notes. Uses simple JSON file-based storage by default.

- Base URL (running container): http://localhost:3001
- Interactive API docs: http://localhost:3001/docs
- OpenAPI spec: http://localhost:3001/openapi.json

## Run

The container is configured to run on port 3001.
If running locally:

```
python run.py
```

Environment variables (optional):
- NOTES_STORAGE_FILE: path to the JSON file for storage (default: data/notes.json)

## Endpoints

- GET /            -> Health check
- GET /notes       -> List notes
- GET /notes/{id}  -> Get note by id
- POST /notes      -> Create note
- PUT /notes/{id}  -> Update note (title and/or content)
- DELETE /notes/{id} -> Delete note

## Models

Note:
```
{
  "id": 1,
  "title": "My Note",
  "content": "Some content",
  "created_at": "2024-01-01T00:00:00+00:00",
  "updated_at": "2024-01-01T00:00:00+00:00"
}
```

## Examples

- Create:
```
curl -X POST http://localhost:3001/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"First","content":"Hello world"}'
```

- List:
```
curl http://localhost:3001/notes
```

- Get by id:
```
curl http://localhost:3001/notes/1
```

- Update:
```
curl -X PUT http://localhost:3001/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated title"}'
```

- Delete:
```
curl -X DELETE http://localhost:3001/notes/1
```

## Validation and Errors

- POST /notes requires non-empty "title" (<= 200 chars) and non-empty "content".
- PUT /notes/{id} requires at least one of "title" or "content" to be provided.
- 404 returned when a note is not found.
- 400 returned for invalid input.

## CORS

CORS is enabled for all origins, suitable for simple frontend integration. Adjust as needed.
