# main.py
import json
from flask import Blueprint, Flask, render_template, request, \
    jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from .controller import get_initial_panels, get_filtered_panels, \
    get_initial_records, get_antibody_conjugate, get_full_data, get_row
from .models import Panel, User
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index_public.html')


@main.route('/panels')
@login_required
def show_panels():
    data = get_full_data()
    panels = Panel.query.all()
    panels = [panel.__dict__ for panel in panels]
    for panel in panels:
        panel["published_by"] = User.query.get(panel["created_by"]).name
        panel["records"] = []
        for id in panel["lab_ids"].split(","):
            panel["records"].append(get_row(data, id))
    return render_template('panels.html', name=current_user.name,
                           root_url=request.url_root,
                           panels=panels)


@main.route('/panel')
@login_required
def show_panel():
    data = get_full_data()
    panel_id = request.args.get("id")
    panel = Panel.query.get(panel_id)
    if panel:
        panel = panel.__dict__
        panel["published_by"] = User.query.get(panel["created_by"]).name
        panel["records"] = []
        for id in panel["lab_ids"].split(","):
            panel["records"].append(get_row(data, id))
        return render_template('panel.html',
                               name=current_user.name,
                               panel=panel, root_url=request.url_root)
    flash(f"No panel found with id {panel_id}", "warning")
    return redirect(url_for('show_panels'))


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
                created_by = current_user.id
                lab_ids = ",".join(lab_ids)
                new_panel = Panel(title=panel_title,
                                  created_by=created_by,
                                  lab_ids=lab_ids)
                db.session.add(new_panel)
                db.session.commit()
                return "success"
        except Exception as ex:
            flash(str(ex), "error")
            return redirect(url_for("main.add_panel"))
    else:
        return render_template('add.html',
                               name=current_user.name,
                               antibodies=antibodies,
                               conjugates=conjugates)
