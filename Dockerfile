FROM python:3.11.0a5-alpine3.14

# Sets environment path to include /usr/bin
ENV PATH="/usr/bin:${PATH}"

# Install Firefox for webscraping
RUN apk update && \
    apk add firefox

# Download and install geckodriver v33 for arm64 architecture
# If you are running 64 bit, not arm64, un-comment the line above and comment the above one out.
RUN apk add --no-cache curl \
    && cd /usr/bin \
    && wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz \
    # && wget -0 geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz # if 64 bit: not arm64 \
    && tar -xzvf geckodriver.tar.gz \
    && rm geckodriver.tar.gz \
    && chmod +x geckodriver \
    && apk del curl


# Ensures that we get the unbuffered python output
ENV PYTHONUNBUFFERED=1

WORKDIR /django

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt