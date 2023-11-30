# undeniab.ly

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

**undeniab.ly** is an in-progress social media links platform.

this project is developed primarily by [Yoru](https://github.com/yo-ru),
his aim is to create the most easy to use, customizable, reliable, and feature-rich
social media links platform.

# Prerequisites
knowledge of linux, python, and databases will certainly help, but are by no means required.

this guide will be targeted towards ubuntu (22.04) - other distros may have slightly different setup processes.

# Requirements
we aim to minimize our dependencies, but still rely on ones such as
- python (programming language)
- node (tailwind css)
- mysql (relational database)
- nginx (http(s) reverse proxy)

# Installation
## installing undeniab.ly's requirements
```sh
# refresh local package index & upgrade packages
sudo apt update && sudo apt upgrade -y

# install required packages
sudo apt install -y python3.12 nodejs \
                    build-essential \
                    mysql-server \
                    nginx

# make sure pip, setuptools, & pipenv are up to date
python3.12 -m pip install -U pip setuptools pipenv

# install undeniab.ly's dependencies (python-specific & node-specific)
make install
```

## creating a database for undeniab.ly
you will need to create a database for undeniab.ly to store persistent data.
```sh
# start mysql
sudo service mysql start

# login to mysql's shell with root - the default admin account

# note that this shell can be rather dangerous - it allows users
# to perform arbitrary sql commands to interact with the database.

# it's also very useful, powerful, and quick when used correctly.
sudo mysql
```
from this mysql shell, we'll want to create a database, a user account, and give the user full permissions to the database.

then, later on, we'll configure undeniab.ly to use this database as well.
```sql
# you'll need to change:
# - YOUR_DB_NAME
# - YOUR_DB_USER
# - YOUR_DB_PASS

# create a database for undeniab.ly to use
CREATE DATABASE YOUR_DB_NAME;

# create a user to use the undeniab.ly database
CREATE USER 'YOUR_DB_USER'@'localhost' IDENTIFIED BY 'YOUR_DB_PASS';

# grant the user full access to all tables in the undeniab.ly database
GRANT ALL PRIVILEGES ON YOUR_DB_NAME.* TO 'YOUR_DB_USER'@'localhost';

# make sure privilege changes are applied immediately
FLUSH PRIVILEGES;

# exit the mysql shell, back to bash
quit
```

## setting up the database structure for undeniab.ly
we've now created an empty database - databases are full of 2-dimensional tables of data.

undeniab.ly has many tables it uses to organize information.

the columns (vertical) represent the types of data stored, for example, the privileges of a `user`.

the rows (horizontal) represent the individual items or events in a table, for example, the individual user in the `users` table.

the base state of the database is stored in `ext/base.sql`; it's a bunch of sql commands that can be run in sequence to create the base state we want.
```sh
# you'll need to change
# - YOUR_DB_NAME
# - YOUR_DB_USER

# import undeniab.ly's mysql structure to our new db
# this runs the contents of the file as sql commands.
mysql -u YOUR_DB_USER -p YOUR_DB_NAME < ext/base.sql
```

## configuring a reverse proxy (we'll use nginx)
undeniab.ly relies on a reverse proxy for tls (https) support, and for ease-of-use in terms of configuration. nginx is an open source and efficent web server we'll be using for this guide, but feel free to check out others, like caddy or apache.
```sh
# copy the example nginx config to /etc/nginx/sites-available,
# and make a symbolic link to /etc/nginx/sites-enabled
sudo cp ext/nginx.conf /etc/nginx/sites-available/undeniably.conf
sudo ln -s /etc/nginx/sites-available/undeniably.conf /etc/nginx/sites-enabled/undeniably.conf

# now, you can edit the config file.
# the spots you'll need to change are marked.
sudo nano /etc/nginx/sites-available/undeniably.conf

# reload config from disk
sudo nginx -s reload
```

## configure undeniab.ly
all configuration for undeniab.ly itself can be done from the `.env` file. we provide an example `.env.example` file which you can use as a base.
```sh
# create a configuration file from the sample provided
cp .env.example .env

# you'll want to configure, at least, all the database related fields (DB_*).

# open the configuration file for editing
nano .env
```

## congratulations! you're finished
if everything went well, you should be able to start undeniab.ly:
```sh
# start undeniab.ly
make run
```
