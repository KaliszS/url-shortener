# url-shortener

DRF example application to shorten urls.

### Requirements
- python 3.13
- uv

### Installation
```bash
uv sync
```

### Preparing to use
```bash
# migrate to database
uv run manage.py migrate

# run the server
uv run manage.py runserver

# run tests (optional)
uv run manage.py test shortener
```

### API Endpoints

#### Create Shortened URL
```
POST /api/shorturls/

Request:
{
    "url": "https://www.django-rest-framework.org/"
}

Response:
{
    "original_url": "https://www.django-rest-framework.org/",
    "hash": "de1caf",
    "_links": {
        "self": "http://localhost:8000/api/shorturls/de1caf/",
        "redirect": "http://localhost:8000/de1caf"
    }
}
```

#### Get Original URL
```
GET /api/shorturls/{hash}/

Response:
{
    "original_url": "https://www.django-rest-framework.org/",
    "_links": {
        "self": "http://localhost:8000/api/shorturls/de1caf/",
        "redirect": "http://localhost:8000/de1caf"
    }
}
```

#### Delete Shortened URL
```
DELETE /api/shorturls/{hash}/

Response: 204 No Content
```

#### Redirect to Original URL
```
GET /{hash}/

Response: 302 Found
Location: https://www.django-rest-framework.org/
```

### Usage Examples
```bash
# create short url
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://www.django-rest-framework.org/"}' http://localhost:8000/api/shorturls/

# get original url from hash
curl http://localhost:8000/api/shorturls/de1caf/

# redirect to original url
curl -L http://localhost:8000/de1caf

# remove short url
curl -X DELETE http://localhost:8000/api/shorturls/de1caf/
```

### Development

#### Code Quality
```bash
# install dev dependencies
uv sync --dev

# run linter
uv run ruff check

# run formatter
uv run ruff format
```

The project includes a GitHub Actions pipeline that runs:
- tests
- linter check
- formatter check
