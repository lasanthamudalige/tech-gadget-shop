# Tech Haven

A Tech gadget shop program using [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.2.x/), [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) and [Stripe API](https://stripe.com/payments/checkout).

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Usage](#usage)

## General info

User can register, login, add items to the cart and buy items on the website and admin can add/edit/delete new items on the store.

## Technologies
Project is created with:
* Python version: >= 3.10
* Flask version: 2.2.2
* Stripe API

## Screenshots

- ***Admin panel preview and function***
	- ![ezgif com-crop](https://github.com/lasanthamudalige/tech-gadget-shop/assets/91461938/ab458f3e-1eb1-46b9-a81f-41e34e17ba5b)

- ***Normal user interactions***
	- ![ezgif com-crop(1)](https://github.com/lasanthamudalige/tech-gadget-shop/assets/91461938/ba91abae-8d1a-4245-863f-ec7059a7f084)

## Setup

To clone and run this application, you'll need [Git](https://git-scm.com) installed on your computer.\
From your command line run:

* Clone this repository
```bsah
git clone https://github.com/lasanthamudalige/tech-gadget-shop.git
```

* Go into the repository
```bash
cd tech-gadget-shop/
```

* To install all dependencies using pip
```bash
pip install -r requirements.txt
```

* To install all dependencies to current environment using miniconda
```bash
conda env update -n my_env --file environment.yaml
```


## Usage

To run this project in Linux/Unix:
```bash
python3 server.py
```

To run this project in Windows:
```bash
python server.py
```

## License 
This project is open source and available under the [MIT License](https://github.com/lasanthamudalige/tech-gadget-shop/blob/main/LICENSE).
