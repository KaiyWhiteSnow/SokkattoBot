if __name__ == '__main__':
    from . import logger
    from . import app
    logger.debug("Running app")
    app.run(debug=True)