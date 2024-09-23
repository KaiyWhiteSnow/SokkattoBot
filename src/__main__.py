if __name__ == '__main__':
    import logging
    from .config.logger_config import configure_logger
    # Configure loggers - This must run before SQLAlchemy is initialized
    configure_logger(
        [
            "Sokkatto.manager",
            "Sokkatto.factory",
            "Sokkatto.login",
            "Sokkatto",
            "Sokkatto.database",
            "sqlalchemy"
        ]
    )

    logger: logging.Logger = logging.getLogger("Sokkatto")
    logger.info("Logger ready")
    from . import app
    app.run(debug=False)