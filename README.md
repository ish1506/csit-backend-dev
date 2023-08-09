## Introduction
This is a simple RESTful API server built for the [CSIT Mini Challenge](https://www.csit.gov.sg/events/csit-mini-challenge) on Backend Development in Jul 2023. I used the Challenge as an opportunity to learn Flask, MongoDB and Docker.

## Getting Started

### Pre-requisites
- Python 3
- Docker (optional)

### Installation
Building from source:
1. Clone this repository.
    ```bash
    git clone git@github.com:ish1506/csit-backend-dev.git
    ```
2. Install the dependencies.
    ```bash
    cd csit-backend-dev
    pip install -r requirements.txt
    ```
3. Start the server.
    ```bash
    python3 server.py
    ```

Alternatively, using Docker:
```bash
docker pull ish1506/csit-backend-dev
docker run -p 8080:8080 ish1506/csit-backend-dev
```

### Usage
Sample requests:
- `http://127.0.0.1:8080/flight?departureDate=2023-12-10&returnDate=2023-12-16&destination=Frankfurt`
- `http://127.0.0.1:8080/hotel?checkInDate=2023-12-10&checkOutDate=2023-12-16&destination=Abu+Dhabi`