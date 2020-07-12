# A Python and Django Store API Example

## Installation

```bash

# Clone de repository
git clone https://github.com/gustavo-fonseca/python-store

# Go to project`s folder and copy .env.example to .env
cd /project-folder
cp .env.example .env

# Run docker-compose and make the initial migrations
docker-compose up -d
docker exec store_backend python manage.py makemigrations
docker exec store_backend python manage.py migrate
docker exec store_backend python manage.py loaddata initial.json

# Running in development mode
docker exec -it store_backend python manage.py runserver 0:8000

```

## Features

### User
- [x] List 
- [x] Read 
- [x] Create 
- [x] Update 
- [x] Delete (Soft)
- [x] Forget password (Send link to email)
- [x] Reset password
- [x] Login
- [x] Token refresh
- [ ] Test
- [ ] Docs

### ClientProfile
- [x] List 
- [x] Read 
- [x] Create 
- [x] Update 
- [ ] Test
- [ ] Docs

### Client Address
- [ ] List 
- [ ] Read 
- [ ] Create 
- [ ] Update 
- [ ] Delete (Soft)
- [ ] Test
- [ ] Docs

### Products
- [ ] List 
- [ ] Read 
- [ ] Create 
- [ ] Update 
- [ ] Delete (Soft)
- [ ] Test
- [ ] Docs

### Order (Pedido)
- [ ] List 
- [ ] Read 
- [ ] Create 
- [ ] Update 
- [ ] Close
- [ ] Payment
- [ ] Test
- [ ] Docs

### Payment Method
- [ ] Pagseguro
- [ ] Paypall
