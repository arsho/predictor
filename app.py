import json
from flask import Flask, render_template, request, jsonify, url_for, redirect, flash
from controller import get_initial_panels, get_filtered_panels

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "primary_form" in request.form:
            antibodies = [s.strip() for s in request.form["antibody"].split(",")]
            panels = get_initial_panels(antibodies)
            return render_template('index.html', panels=panels, old_patterns="CD103:APC,CD11c:PE-Cy7")
        elif "secondary_form" in request.form:
            panels = json.loads(request.form["old_panels"].replace("\'", "\""))
            old_patterns = request.form["patterns"]
            patterns = old_patterns.split(",")
            criteria = []
            for pattern in patterns:
                antibody, conjugate = pattern.split(":")
                criteria.append((antibody.strip(), conjugate.strip()))
            panels = get_filtered_panels(panels, criteria)
            return render_template('index.html', panels=panels, old_patterns=old_patterns)
    return render_template('index.html')
