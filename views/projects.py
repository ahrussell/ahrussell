from flask import Blueprint, render_template, request
import random
import json
import uuid

import sys

projects = Blueprint('projects', __name__, subdomain='', url_prefix='/projects')

@projects.route('/')
@projects.route('/<page_name>')
def index(page_name=None):
    if page_name == None:
        return render_template("projects.html", page_name="projects")
    else:
        return render_template("/projects/%s.html" % page_name, page_name=page_name)


@projects.route('/lincoln/run', methods=['GET', 'POST'])
def run_lincoln():
    page_name = "lincoln"

    if request.method == "POST":
        # return json.dumps(sys.path)
        import src.lincolnbot as lincolnbot

        files = []

        for c in request.form.iteritems():
            f = c[0]
            v = c[1]

            if f == "order":
                order = int(v)
            else:
                files.append("src/lincolnbot/speeches/"+f+".txt")

        bot = lincolnbot.LincolnBot(files, order)

        speech = ""

        for i in range(random.randint(5, 7)):
            speech += bot.write_sentence().capitalize() + " "

        return speech
    else:
        return render_template("/projects/%s_run.html" % page_name, page_name=page_name, forms = request.form, post=False)

@projects.route('/fifthseason/run/<fn>', methods=['GET'])
def get_music(fn):
    return render_template("/projects/fifthseason/sheet_music_printer.html", fn = fn)

@projects.route('/fifthseason/run', methods=['GET', 'POST'])
def run_fifthseason():
    page_name = "fifthseason"

    if request.method == "POST":
        import src.fifthseason as fifthseason

        files = {}

        for c in request.form.iteritems():
            f = c[0]
            v = c[1]

            files[f] = "src/fifthseason/music/"+f+".json"

        bot = fifthseason.Composer(files)
        piece = bot.measurify(bot.write(350), 4, 4)

        json_file = uuid.uuid4().hex

        fp = open("static/projects/fifthseason/output/json/"+json_file+".json", "w")

        json.dump(piece, fp)

        fp.close()

        return json_file
    else:
        return render_template("/projects/%s_run.html" % page_name, page_name=page_name, forms = request.form, post=False)



