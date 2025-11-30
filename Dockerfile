FROM praekeltfoundation/python-base:3

# Copy in the required files
RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /app
WORKDIR /app

# RUN pipenv install --system --deploy --ignore-pipfile
RUN pipenv install
EXPOSE 8080
RUN pipenv install gunicorn

# CMD pipenv run python response_handler.py
CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8080", "response_handler:app"]
