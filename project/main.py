# main.py
import json
from flask import Blueprint, Flask, render_template, request, \
    jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from .controller import get_initial_panels, get_filtered_panels, \
    get_initial_records, get_antibody_conjugate
from .models import Panel
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index_public.html')


@main.route('/panels')
@login_required
def show_panels():
    panels = Panel.query.all()
    return render_template('panels.html', name=current_user.name,
                           panels=panels)


@main.route('/add', methods=["GET", "POST"])
@login_required
def add_panel():
    antibodies, conjugates = get_antibody_conjugate()
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
                                       name=current_user.name,
                                       antibodies=antibodies,
                                       conjugates=conjugates)
            elif "secondary_form" in request.form:
                lab_ids = request.form.getlist("selected_lab_ids")
                panel_title = request.form.get("panel_title")
                created_by = current_user.name
                contact_email = current_user.email
                output = f"title: {panel_title}, ids: "
                lab_ids = ",".join(lab_ids)
                output += f"{lab_ids}"
                output += f", created by: {created_by}({contact_email})"
                new_panel = Panel(title=panel_title,
                                  contact_email=contact_email,
                                  created_by=created_by,
                                  lab_ids=lab_ids)
                db.session.add(new_panel)
                db.session.commit()
                return output
        except Exception as ex:
            flash(str(ex), "error")
            return redirect(url_for("main.add_panel"))
    else:
        return render_template('add.html',
                               name=current_user.name,
                               antibodies=antibodies,
                               conjugates=conjugates)
