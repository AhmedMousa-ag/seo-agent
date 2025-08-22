FROM python:3.11-slim

# Add user seo
RUN useradd -m seo

WORKDIR /home/seo/app

RUN chown -R seo:seo /home/seo

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .
RUN chown -R seo:seo /home/seo/app

USER seo
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
