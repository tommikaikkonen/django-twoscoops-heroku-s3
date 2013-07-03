========================
Django-Heroku-S3-EmailRegistration Project Template
========================

This is a fork of the Two Scoops Django 1.5 project template with lots of inspiration from Django Modern Template. This is mainly for my personal use, so make sure to test properly if you want to use this.

Features:

Ready to deploy to Heroku
S3 for storage
Customer user with email as username
User registration, profiles and base templates
Compass/Sass
Bootstrap



A project template for Django 1.5.

To use this project follow these steps:

#. Create your working environment
#. Install Django
#. Create the new project using the django-two-scoops template
#. Install additional dependencies
#. Use the Django admin to create the project

*note: these instructions show creation of a project called "icecream".  You
should replace this name with the actual name of your project.*

Working Environment
===================

You have several options in setting up your working environment.  We recommend
using virtualenv to seperate the dependencies of your project from your system's
python environment.  If on Linux or Mac OS X, you can also use virtualenvwrapper to help manage multiple virtualenvs across different projects.

Virtualenv Only
---------------

First, make sure you are using virtualenv (http://www.virtualenv.org). Once
that's installed, create your virtualenv::

    $ virtualenv --distribute icecream

You will also need to ensure that the virtualenv has the project directory
added to the path. Adding the project directory will allow `django-admin.py` to
be able to change settings using the `--settings` flag.

Virtualenv with virtualenvwrapper
--------------------------

In Linux and Mac OSX, you can install virtualenvwrapper (http://virtualenvwrapper.readthedocs.org/en/latest/),
which will take care of managing your virtual environments and adding the
project path to the `site-directory` for you::

    $ mkdir icecream
    $ mkvirtualenv -a icecream icecream-dev
    $ cd icecream && add2virtualenv `pwd`

Windows
----------

In Windows, or if you're not comfortable using the command line, you will need
to add a `.pth` file to the `site-packages` of your virtualenv. If you have
been following the book's example for the virtualenv directory (pg. 12), then
you will need to add a python pathfile named `_virtualenv_path_extensions.pth`
to the `site-packages`. If you have been following the book, then your
virtualenv folder will be something like::

`~/.virtualenvs/icecream/lib/python2.7/site-directory/`

In the pathfile, you will want to include the following code (from
virtualenvwrapper):

    import sys; sys.__plen = len(sys.path)
    /home/<youruser>/icecream/icecream/
    import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)

Installing Django
=================

To install Django in the new virtual environment, run the following command::

    $ pip install django

Creating your project
=====================

To create a new Django project called '**icecream**' using
django-twoscoops-project, run the following command::

    $ django-admin.py startproject --template=https://github.com/tommikaikkonen/django-twoscoops-heroku-s3/archive/develop.zip --extension=py,rst,html,dotfile,rb --name=Procfile,Gemfile icecream

Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*


Heroku setup
============

    heroku apps:create <project_name> --buildpack=git://github.com/heroku/heroku-buildpack-python.git
    heroku addons:add memcachier:dev
    heroku addons:add sendgrid:starter
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups:auto-month
    heroku addons:add newrelic:standard
    heroku config:add AWS_ACCESS_KEY_ID=<key id>
    heroku config:add AWS_SECRET_ACCESS_KEY=<secret key>
    heroku config:add AWS_STORAGE_BUCKET_NAME=<bucket name>
    setopt rcquotes
    heroku config:add SECRET_KEY=<secret_key>
    heroku run python <project_name>/manage.py syncdb --settings=<project_name>.settings.production
    heroku run python <project_name>/manage.py migrate --settings=<project_name>.settings.production
    heroku run python <project_name>/manage.py createsuperuser --settings=<project_name>.settings.production
    heroku run python <project_name>/manage.py collectstatic --settings=<project_name>.settings.production

    Log into admin and change the site model from the default "example.com" to the proper url and name.

Acknowledgements
================

    - Many thanks to Randall Degges for the inspiration to write the book and django-skel.
    - All of the contributors_ to this project.

.. _contributors: https://github.com/twoscoops/django-twoscoops-project/blob/master/CONTRIBUTORS.txt
