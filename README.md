# Wish (Item Catalog)

This is a Prerequisite for Udacity's Full Stack Developer nano-degree.
Wish is an application that provides a list of jewelry items within a variety of categories, as well as provide a user registration and authentication system.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* [Vagrant](https://www.vagrantup.com)
* [VirtualBox](https://www.virtualbox.org) - Virtual Machine


### Installing

1. Install [Vagrant](https://www.vagrantup.com/downloads.html)
2. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3. Download [FSND virtual machine](https://github.com/udacity/fullstack-nanodegree-vm)
4. Clone this repository to vagrant shared directory
5. In your terminal, navigate to FSND virtual machine folder then type the following commands:
```
cd vagrant
vagrant up
vagrant ssh
cd /vagrant/Wish
```
6. Run the database setup:
```
python database_setup.py
```
7. Add some data:
```
python seeder.py
```
8. Run the application
```
python application.py
```
9. Access and test the application by visiting http://localhost:5000 locally

## API endpoints
* /catalog/json
return all the data in the database (categories & items) in the following format:
```
{
  categories:
  [
    {
      id: ""
      name: ""
      items:
      [
        {
          id: ""
          title: ""
          description: ""
        }
      ]
    }
  ]
}
```
* /catalog/<string:category_name>/json
return all the items for the given category in the following format:
```
{
  category:
    {
      id: ""
      name: ""
      items:
      [
        {
          id: ""
          title: ""
          description: ""
        }
      ]
    }
}
```

## Built With

* [Flask](http://flask.pocoo.org) - The used python framework

## Acknowledgments

* [colorlib](https://colorlib.com) - The used HTML template
