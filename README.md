# Inventory API (Flask)

## About

This is a simple inventory API made using Python and Flask.
It allows basic CRUD operations and also connects to an external product API.

## Features

* View all items
* Add new items
* Update items
* Delete items
* Fetch product info from OpenFoodFacts API
* Simple CLI to use the API

## Setup

```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```
## Run App

```bash
python app.py

Open:
http://127.0.0.1:5000

## CLI

```bash
python cli.py
```
## Tests

```bash
pytest
```
## Project Files

* app.py
* cli.py
* inventory.py
* services/openfoodfacts.py
* test_app.py
