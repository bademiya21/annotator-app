# Simple Text Annotator App in Flask

This flask app is a simple personal project (done by Andrew Tan[@a-tanman] and myself) that is meant to make it easier to label/annotate text data for creating datasets for supervised machine learning.

Based on a flask-bootstrap template by Mark Brinkmann (https://pythonhosted.org/Flask-Bootstrap/).

### Installing Dependences

Install dependences from requirements.txt using 

```pip3 install -r requirements.txt```

### Running

From main folder directory, you can run the app on port 5000 with:

```python application.py```

Some mock data is found in the main folder for you to test out.

### Key Features

- Allows user to upload .csv or Excel files and view samples of the data. Do make sure that the encoding of the csv file is in the UTF-8 format.
- Users can select one column of interest to create label for this column. Only one label can be tagged per row.
- A separate .csv file is created with the results of the labelling. This file is written to each time you label one row.
- You have the option to add more labels as you progress.
- If you close the program and start labelling again later, ensure that the data file and username are identical to before, and you should be able to continue from where you last stopped
- Once the entire data has been labelled, the user will be presented with links to download the labelled data and to delete all files (original and labelled) from the server. Remember to download first before deleting the files!

### Known Issues

In some cases, there are issues with reading csv files that have the wrong encoding. It expects files to be 'UTF-8' encoded.

Your session may also end if you do not use the program for a while, and you'll need to upload the file again.

### Note

Please feel free to contribute to this project, and let me know if there are bugs or feature requests.