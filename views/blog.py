from flask import Blueprint, render_template
import markdown
import os
from datetime import date

from ahrussell import app

blog = Blueprint('blog', __name__, subdomain='', url_prefix='/blog')

home_dir = app.config["HOME"]

@blog.route('/')
def index():

    return render_template("blog.html", page_name="blog")


@blog.route('/<yyyy>/<mm>/<dd>/<title>')
def post(yyyy, mm, dd, title):

    with open(home_dir+"_blog/"+yyyy+"-"+mm+"-"+dd+"-"+title+".md") as f:
        d = date(int(yyyy), int(mm), int(dd)).strftime("%a %B %d, %Y")

        return render_template("post.html", post=markdown.markdown(f.read()), page_name="blog", formatted_date=d)


