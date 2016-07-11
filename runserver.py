from intz import app
# from intz-dev import dev-app
import os


port = int(os.environ.get('PORT', 5000))
# dev-app.run(host='0.0.0.0', port=port, threaded=True)
app.run(host='0.0.0.0', port=port, threaded=True)
