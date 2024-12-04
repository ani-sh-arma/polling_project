FROM python:3.11-alpine AS builder

ENV DONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
 
# RUN python3 -m venv venv
# ENV VIRTUAL_ENV=/app/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
 
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
 
# Stage 2
# FROM python:3-alpine AS runner
 
# WORKDIR /app
 
# COPY --from=builder /app/venv venv
# COPY polling_project polling_project
 
# ENV VIRTUAL_ENV=/app/venv
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"
# ENV PORT=8000
 
# EXPOSE ${PORT}
EXPOSE 8000
 
# CMD gunicorn --bind :${PORT} --workers 2 polling_project.wsgi
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
