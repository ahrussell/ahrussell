from flask import Blueprint, render_template

blog = Blueprint('blog', __name__, subdomain='', url_prefix='/blog')

@blog.route('/')
@blog.route('/<int:post_id>')
def index(post_id = None):

    return render_template("blog.html", page_name="blog", posts=[])

