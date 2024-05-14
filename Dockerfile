FROM python
LABEL author="wildmuff"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP /app/nettrackercore/api/app.py

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "5000"]
