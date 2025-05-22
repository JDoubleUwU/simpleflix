from flask import Flask, render_template
from webserver.webcontroller import webcontroller_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# blueprint registration
app.register_blueprint(webcontroller_bp)

if __name__ == '__main__':
    app.run(debug=True)
    #pp.run()
