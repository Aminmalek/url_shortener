# URL Shortener Service

## Overview

This URL Shortener Service allows users to shorten long URLs efficiently. Built with FastAPI, it provides an API endpoint for generating short URLs and a redirect mechanism for retrieving original URLs. The service implements a reliable retry mechanism to handle potential conflicts and utilizes caching to enhance performance and scalability.

## Features

- **Shorten URLs**: Generate unique short URLs from long URLs.
- **Redirect**: Redirect users from short URLs to the original URLs.
- **Retry Mechanism**: Ensures reliability by attempting to generate a unique short URL multiple times in case of collisions.
- **Caching**: Improves performance and scalability by storing frequently accessed data in memory.

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy**: ORM for database interactions.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **Starlette**: For the HTTP response handling.
- **Redis (or another cache solution)**: Used for caching short URLs to improve performance.

## Installation and Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/url-shortener.git
   cd url-shortener
   docker compose up --build
2. Running tests 

   ```bash 
   docker exec -it url-app python -m unittest discover tests
## Retry Mechanism
The service implements a retry mechanism in the shorten_url_with_retry function. If generating a short URL results in a collision (due to unique constraints), the service will automatically retry generating a new short URL up to a predefined limit (MAX_RETRIES). This ensures that the service remains reliable and minimizes user frustration when encountering duplicate entries.

## Caching for Performance and Scalability
To enhance performance, the service employs a caching strategy that stores frequently accessed short URLs in memory. When a user attempts to access a short URL, the service first checks the cache before querying the database. This cache-aside pattern not only reduces latency for users but also decreases the load on the database, allowing the service to scale more efficiently.

