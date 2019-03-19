# Simple Text Annotator App in Flask

This flask app is a simple personal project (done by Andrew Tan[@a-tanman] and myself) that is meant to make it easier to label/annotate text data for creating datasets for supervised machine learning.

Based on a flask-bootstrap template by Mark Brinkmann (https://pythonhosted.org/Flask-Bootstrap/). Most of the other features have been adapted from [Miguel's blog](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). This app has been developed in a virtual environment in Windows and deployed in AWS using an Ubuntu MI.

### Installing Dependences

This project requires Python 3x to be installed in the system. If your operating system does not provide you with a Python package, you can download an installer from the [Python official website](http://python.org/download/).

This app is best used in a virtual environment. To create one in the project directory, type the following command in the terminal:

```$ python3 -m venv textannoenv```

Note that in some operating systems you may need to use python3 instead of python in the command above.

To activate your virtual environment, you use the following command:

```$ source textannoenv/bin/activate```

If you are using a Microsoft Windows command prompt window, the activation command is slightly different:

```$ textannoenv\Scripts\activate```

Once the virtual environment has been activated, install the dependencies from requirements.txt using 

```pip install -r requirements.txt```

###	Initialization
As the app contains a user-registration feature, the user database needs to be initialized. Create the migration repository for annotator_app by running *flask db init* in the terminal window. You should see something like below:

```
(venv) $ flask db init\
  Creating directory /home/<user>/annotator_app/migrations ... done\
  Creating directory /home/<user>/annotator_app/migrations/versions ... done\
  Generating /home/<user>/annotator_app/migrations/alembic.ini ... done\
  Generating /home/<user>/annotator_app/migrations/env.py ... done\
  Generating /home/<user>/annotator_app/migrations/README ... done\
  Generating /home/<user>/annotator_app/migrations/script.py.mako ... done\
  Please edit configuration/connection/logging settings in\
  '/home/<user>/annotator_app/migrations/alembic.ini' before proceeding.\
 ```

After you run this command, you will find a new migrations directory, with a few files and a versions sub-directory inside.

With the migration repository in place, create the first database migration, which will include the users table that maps to the User database model. In this case, since there is no previous database, the automatic migration will add the entire User model to the migration script. The *flask db migrate* sub-command generates these automatic migrations:

```(venv) $ flask db migrate -m "users table"\
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.\
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.\
INFO  [alembic.autogenerate.compare] Detected added table 'user'\
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'\
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'\
  Generating /home/<user>/annotator_app/migrations/versions/e517276bb1c2_users_table.py ... done\
 ```

### Running

Before running, Flask needs to be told how to import it, by setting the FLASK_APP environment variable:

```(venv) $ export FLASK_APP=annotator_app.py```

If you are using Microsoft Windows, use set instead of export in the command above.

You can run the app with the following command:

```(venv) $ flask run```

Open up your web browser and enter the following URL in the address field:

```http://localhost:5000/```

Some mock data is found in the main folder for you to test out.

### Key Features

-	User-registration system in-built for security
- 	Allows registered user to upload .csv or Excel files and view samples of the data. Do make sure that the encoding of the csv file is in the UTF-8 format.
- 	Users can select one column of interest to create label for this column. Only one label can be tagged per row.
- 	A separate .csv file is created with the results of the labelling. This file is written to each time you label one row.
- 	You have the option to add more labels as you progress.
- 	If you close the program and start labelling again later, ensure that the data file and username are identical to before, and you should be able to continue from where you last stopped
- 	Once the entire data has been labelled, the user will be presented with links to download the labelled data and to delete all files (original and labelled) from the server. Remember to download first before deleting the files!

### Known Issues

In some cases, there are issues with reading csv files that have the wrong encoding. It expects files to be 'UTF-8' encoded.

Your session may also end if you do not use the program for a while, and you'll need to upload the file again.

### Note

Please feel free to contribute to this project, and let me know if there are bugs or feature requests.
