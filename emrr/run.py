from backend.auth import app, db
# from backend.auth import defaultHandler
import logging
import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=int(os.environ.get('PORT', 1337)), debug=True, threaded=True)
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    # app.register_error_handler(Exception, defaultHandler)
    # app.logger.basicConfig(level=logging.ERROR)