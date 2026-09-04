FROM python:3.11-slim
WORKDIR /CrossJoin
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "CrossJoin_App.py"]
