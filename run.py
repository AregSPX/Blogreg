from flaskblog import create_app    # when importing from package (folder), it looks at __init__.py

app = create_app()                  # we imported the app creator function and initialized an app with our default configs

if __name__ == '__main__':   # this file's only purpose is to run the app
    app.run(debug=False)
