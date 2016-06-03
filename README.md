Mom-backend - Mom is a Organization Manager
===========================================

Mom-backend is a Django backend used by the [Mom](https://github.com/Richard-Degenne/mom)
Android application.

About
-----

This is a school project for IG2I, a computer sciences engineering school
in nothern France.

Installation
------------

### Getting the software

In order to get mom-backend, you can

- Run `$ git clone https://github.com/Richard-Degenne/mom-backend/tree/v0.2` ;
- Donwload a ZIP archive by clicking [here](https://github.com/Richard-Degenne/mom-backend/tree/v0.2)

Position into the mom-backed folder by running

    $ cd mom-backend

### Installing dependancies

Make sure you have [pip](https://pip.pypa.io) installed. Then run

    $ pip install -r requirements.txt

This will install every library mom-backend needs to run. It can take a while.

### Setting up a database

Create a file in the `mom` folder, called `secrets.py`. In this file, write the following

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '<database_name>',
            'USER': '<database_user>',
            'PASSWORD': '<database_user_password>',
            'HOST': '<database_host>',
            'PORT': '<database_port>',
        }
    }

and replace every angle-bracketed name with consistent values.

Save the file and then run

    $ python manage.py migrate

This is set up the database for mom-backend. It can take a while.

### Setting up a Google API key

Since mom-backend uses the Google API, you need a valid Google API key. Open again the `secrets.py` file, and add the following line.

    google_api_key = "<google_api_key>"

Replace the angle-bracketed value by the actual key.

### Running the server

That's it! You're all set up! You can now run the mom-backend server with the following command.

    $ python manage.py runserver 0.0.0.0:8000

The server will remain active until you `<Ctrl-C>` out of it.
