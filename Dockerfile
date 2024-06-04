FROM python:3.11-slim

# Create a new group and user
RUN groupadd -r appgroup && useradd -m -r -g appgroup appuser

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Change ownership of the app directory
RUN chown -R appuser:appgroup /app

# Switch to appuser
USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
