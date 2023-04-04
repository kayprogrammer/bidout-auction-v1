# BidOut Auction V1 (MVT)

![alt text](https://github.com/kayprogrammer/bidout-auction-v1/blob/main/display.png?raw=true)


#### Django Docs: [Documentation](https://docs.djangoproject.com/en/4.2/)

#### PG ADMIN: [pgadmin.org](https://www.pgadmin.org) 


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
- Create an `.env` file and copy the contents from the `.env.example` to the file and set the respective values. A postgres database can be created with PG ADMIN or psql

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