## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python: Flask is a Python web framework, so you'll need Python installed. You can download it from [Python's official website](https://www.python.org/downloads/).

## Step 1: Install Flask

With your virtual environment activated, you can now install Flask. Run the following command:

```bash
pip install Flask
```

This command will download and install Flask and its dependencies.

## Step 2: Run the Flask Application

To start your Flask web server, run the following command from the same directory where `main.py` file is located:

```bash
python main.py
```

You should see output similar to the following:

```
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

This means your Flask web server is running locally at `http://127.0.0.1:5000/`. The web server will give an error because no API is linked to the main page.

## Step 3: Make an API Call

In order to test the functionality of the methods, you have to run the `_test.py` file. The file includes either `GET` or `POST` calls to the APIs.

```bash
python _test.py
```

Each API call will can be called separately in the `_test.py` file to test specific method. To test `exportJS` method call:

```bash
python _test.py exportJS
```

## Info: API call structure

`base` - the base url of the server
`path` - path to the API directories
`name` - name of the API call
`headers` - HTML headers
`data` - payload send to the server
``
