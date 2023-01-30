# main.py
import json
from flask import Blueprint, Flask, render_template, request, jsonify, url_for, \
    redirect, \
    flash
from flask_login import login_required, current_user
from .controller import get_initial_panels, get_filtered_panels, \
    get_initial_records

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index_public.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('index_old.html', name=current_user.name)


@main.route('/add', methods=["GET", "POST"])
@login_required
def add_panel():
    if request.method == "POST":
        try:
            if "primary_form" in request.form:
                search_items = []
                search_items.append([
                    request.form.get("antibody_1", "").strip(),
                    request.form.get("conjugate_1", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_2", "").strip(),
                    request.form.get("conjugate_2", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_3", "").strip(),
                    request.form.get("conjugate_3", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_4", "").strip(),
                    request.form.get("conjugate_4", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_5", "").strip(),
                    request.form.get("conjugate_5", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_6", "").strip(),
                    request.form.get("conjugate_6", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_7", "").strip(),
                    request.form.get("conjugate_7", "").strip()
                ])
                search_items.append([
                    request.form.get("antibody_8", "").strip(),
                    request.form.get("conjugate_8", "").strip()
                ])
                search_items = [item for item in search_items
                                if item[0] != "" and item[1] != ""]
                search_result, not_found = get_initial_records(search_items)

                for item in not_found:
                    flash(f"Antibody:Conjugate "
                          f"<b>{item[0]}:{item[1]}</b> not found", "warning")
                return render_template('add.html', records=search_result,
                                       searched_items=search_items,
                                       name=current_user.name)

                # flash("Primary form submitted", "success")
                # antibody = request.form["antibody"].strip()
                # antibodies = [s.strip() for s in antibody.split(",")]
                # panels, not_found = get_initial_panels(antibodies)
                # for item in not_found:
                #     flash(f"Antibody <b>{item}</b> not found", "warning")
                # return render_template('add.html', panels=panels,
                #                        old_patterns="",
                #                        searched_antibody=antibody,
                #                        name=current_user.name)
            elif "secondary_form" in request.form:
                # flash("Secondary form submitted", "success")
                panels = json.loads(
                    request.form["old_panels"].replace("\'", "\""))
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
                for item in not_found_patterns:
                    flash(f"Pattern <b>{item}</b> not found", "warning")
                return render_template('add.html', panels=panels,
                                       old_patterns=old_patterns,
                                       searched_antibody=searched_antibody,
                                       name=current_user.name)
        except Exception as ex:
            flash(str(ex), "error")
            return redirect(url_for("main.add_panel"))
    else:
        return render_template('add.html', name=current_user.name)
