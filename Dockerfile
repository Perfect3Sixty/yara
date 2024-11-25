FROM python:3.11-slim
RUN addgroup --system app && adduser --system --group app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 7600
COPY minimal_requirements.txt .
RUN pip install --no-cache-dir -r minimal_requirements.txt
COPY . .
RUN chown -R app:app /app
USER app
EXPOSE 7600
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7600"]