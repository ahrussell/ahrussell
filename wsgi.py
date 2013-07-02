from flask import Flask, render_template, send_file, request, abort
from mongokit import Document, Connection
import datetime

app = Flask(__name__)
conn = Connection()

@app.route('/')
def index():
    # latest = get_blog(1)

    index = render_template("index.html", page_name="home")
    return index

@app.route('/projects/')
@app.route('/projects/<page_name>')
def projects(page_name=None):
    if page_name == None:
        return render_template("projects.html", page_name="projects")
    else:
        return render_template("/projects/%s.html" % page_name, page_name=page_name)

@app.route('/projects/lincoln/run', methods=['GET', 'POST'])
def run_lincoln():
    page_name = "lincoln"

    if request.method == "POST":
        import lincoln
        import random

        files = []

        for c in request.form.iteritems():
            f = c[0]
            v = c[1]

            if f == "order":
                order = int(v)
            else:
                files.append("lincoln/speeches/"+f+".txt")

        bot = lincoln.LincolnBot(files, order)

        speech = ""

        for i in range(random.randint(5, 7)):
            speech += bot.write_sentence().capitalize() + " "

        return speech
    else:
        return render_template("/projects/%s_run.html" % page_name, page_name=page_name, forms = request.form, post=False)


@app.route('/projects/fifthseason/run/<fn>', methods=['GET'])
def get_music(fn):
    return render_template("/projects/fifthseason/sheet_music_printer.html", fn = fn)

@app.route('/projects/fifthseason/run', methods=['GET', 'POST'])
def run_fifthseason():
    page_name = "fifthseason"

    if request.method == "POST":
        import fifthseason
        import json
        import uuid

        files = {}

        for c in request.form.iteritems():
            f = c[0]
            v = c[1]

            files[f] = "fifthseason/music/"+f+".txt"

        bot = fifthseason.ComposerBot(files)
        piece = bot.measurify(bot.write(350), 4, 4)

        json_file = uuid.uuid4().hex

        fp = open("static/projects/fifthseason/output/json/"+json_file+".json", "w")

        json.dump(piece, fp)

        fp.close()

        return json_file
    else:
        return render_template("/projects/%s_run.html" % page_name, page_name=page_name, forms = request.form, post=False)


@app.route('/blog/')
@app.route('/blog/<int:post_id>')
def blog(post_id = None):
    # if post_id == None:

    #     posts = get_blog()

    #     return render_template("blog.html", page_name="blog", posts=posts)
    # else:
    #     post=get_blog(post_id)

    #     if post == None:
    #         abort(404)

    return render_template("post.html", page_name="blog", posts=[])
    
@app.route('/about')
def about():
    return render_template("about.html", page_name="about")

@app.route('/resume')
def resume():
    return send_file("downloads/resume.pdf")
    
@app.route('/downloads/<path:filepath>')
def downloads(filepath):
    return send_file("downloads/"+filepath, as_attachment=True)


# def get_blog(post_id=None):
#     if post_id==None:
#         return conn.BlogPost.find()
#     else:

#         for post in conn.BlogPost.find({'id':str(post_id)}):

#             return post


if __name__ == '__main__':
    # app.debug = True
    app.run()
