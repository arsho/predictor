import json
from flask import Flask, render_template, request, jsonify, url_for, redirect, \
    flash, session
from controller import get_initial_panels, get_filtered_panels

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/data', methods=["GET"])
def get_data():
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 12, type=int)
    return get_partial_data(offset, limit)


def get_partial_data(offset, limit):
    return session['panels'][offset:offset + limit]


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if "primary_form" in request.form:
                # CD103,CD11c,CD138,CD5,CD69,CD8a,CD73,CD38
                antibody = request.form["antibody"].strip()
                antibodies = [s.strip() for s in antibody.split(",")]
                panels, not_found = get_initial_panels(antibodies)
                session['panels'] = panels
                total_panels = len(panels)
                panels_chunked = get_partial_data(0, 12)
                for item in not_found:
                    flash(f"Antibody <b>{item}</b> not found", "warning")
                return render_template('index.html',
                                       total_panels=total_panels,
                                       panels=panels_chunked,
                                       old_patterns="",
                                       searched_antibody=antibody)
            elif "secondary_form" in request.form:
                panels = session.get('panels', [])
                old_patterns = request.form["old_patterns"].strip()
                patterns = request.form["patterns"].strip()
                searched_antibody = request.form["searched_antibody"].strip()
                if ":" not in patterns:
                    exception_msg = "Pattern is not correct. Correct pattern "
                    exception_msg += "<i><b>Antibody:Conjugate</b></i>"
                    raise Exception(exception_msg)
                if old_patterns != "":
                    old_patterns = old_patterns + "," + patterns
                else:
                    old_patterns = patterns
                panels, not_found_patterns = get_filtered_panels(panels,
                                                                 patterns)
                session['panels'] = panels
                total_panels = len(panels)
                panels_chunked = get_partial_data(0, 12)
                for item in not_found_patterns:
                    flash(f"Pattern <b>{item}</b> not found", "warning")
                return render_template('index.html', total_panels=total_panels,
                                       panels=panels_chunked,
                                       old_patterns=old_patterns,
                                       searched_antibody=searched_antibody)
        except Exception as ex:
            flash(str(ex), "error")
            return redirect(url_for("index"))
    else:
        return render_template('index.html')
