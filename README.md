# Wish (Item Catalog)

This is a Prerequisite for Udacity's Full Stack Developer nano-degree.
Wish is an application that provides a list of jewelry items within a variety of categories, as well as provide a user registration and authentication system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Vagrant
* VirtualBox


### Installing

1. Install Vagrant and VirtualBox
2. Clone this repository to vagrant shared directory
3. Launch the Vagrant VM (vagrant up & vagrant ssh)
4. Navigate to the repository folder
5. Run the database setup:
```
python database_setup.py
```
6. Add some data:
```
python seeder.py
```
7. Run the application
```
python application.py
```
8. Access and test the application by visiting http://localhost:5000 locally

## Built With

* [Flask](http://flask.pocoo.org) - The used python framework

## Acknowledgments

* [colorlib](https://colorlib.com) - The used HTML template
