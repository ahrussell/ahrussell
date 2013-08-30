from flask import Flask, render_template, send_file, request, abort, jsonify
import datetime
import random
import json
import uuid
import markdown

import src

app = Flask(__name__)

app.config['HOME'] = "/var/www/ahrussell/ahrussell/"
# app.config['HOME'] = "/Users/Andrew/Projects/ahrussell/"

from views.projects import projects
app.register_blueprint(projects)
from views.blog import blog
app.register_blueprint(blog)

@app.route('/')
def index():
    home_dir = app.config["HOME"]

    with open(home_dir+"_blog/2014-08-30-fp.md") as f:
        d = date(2014, 8, 30).strftime("%a %B %Y")

        return render_template("index.html", post=markdown.markdown(f.read()), page_name="blog", formatted_date=d)

    
@app.route('/about')
def about():
    return render_template("about.html", page_name="about")

@app.route('/resume')
def resume():
    return send_file("downloads/resume.pdf")
    
@app.route('/downloads/<path:filepath>')
def downloads(filepath):
    return send_file("downloads/"+filepath, as_attachment=True)

@app.errorhandler(404)
@app.errorhandler(403)
@app.errorhandler(410)
def error_page(e):
    error = e.code

    return render_template("error/"+str(error)+".html", page_name="error", error_message=str(e), error=error), int(error)

@app.errorhandler(500)
def error_page2(e):

    print e

    return render_template("error/500.html", page_name="error", error_message=str(500), error="Internal server error"), 500

if __name__ == '__main__':
    app.debug = True
    app.run(port=3333)
