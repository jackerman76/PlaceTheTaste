#!/bin/bash
gunicorn --bind localhost:8080 wsgi:app
