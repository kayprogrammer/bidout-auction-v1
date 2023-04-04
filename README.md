# BidOut Auction V1 (MVT)

![alt text](https://github.com/kayprogrammer/bidout-auction-v1/blob/main/display.png?raw=true)


## How to run locally

* Download this repo or run: 
```bash
    $ git clone git@github.com:kayprogrammer/bidout-auction-v1.git
```

#### In the root directory:
- Install all dependencies
```bash
    $ pip install -r requirements.txt
```
- Create an .env file and copy the contents from the .env.example to the file and set the respective values.

- Create a postgres database with PG ADMIN or psql and add the values to the .env file.

- Run Locally
```bash
    $ python manage.py migrate
```
```bash
    $ python manage.py runserver
```

- Run With Docker
```bash
    $ docker-compose up --build -d --remove-orphans
```
OR
```bash
    $ make build
```