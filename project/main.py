# main.py
import json
from flask import Blueprint, Flask, render_template, request, \
    jsonify, url_for, redirect, flash
from flask_login import login_required, current_user
from .controller import get_initial_panels, get_filtered_panels, \
    get_initial_records, get_antibody_conjugate_mapper, get_full_data, get_row
from .models import Panel, User
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index_public.html')


@main.route('/panels', methods=['GET', 'POST'])
@login_required
def show_panels():
    data = get_full_data()
    page_title = "All Public Panels"
    if request.method == 'POST':
        title = request.form['search_title']
        panels = Panel.query.filter_by(is_publish=True).filter(
            Panel.title.contains(title)).order_by(
            Panel.created_at.desc()).all()
        page_title = f"Search results for public panels with title <i>{title}</i>"
    else:
        panels = Panel.query.filter_by(is_publish=True).order_by(
            Panel.created_at.desc()).all()
    panels = [panel.__dict__ for panel in panels]
    for panel in panels:
        panel["published_by"] = User.query.get(panel["created_by"]).name
        panel["records"] = []
        for id in panel["lab_ids"].split(","):
            panel["records"].append(get_row(data, id))
    return render_template('panels.html', name=current_user.name,
                           current_user_id=current_user.id,
                           root_url=request.url_root,
                           panels=panels, page_title=page_title,
                           only_public_panels=True)


@main.route('/my_panels')
@login_required
def show_my_panels():
    data = get_full_data()
    current_user_id = current_user.id
    panels = Panel.query.filter_by(created_by=current_user_id).order_by(
        Panel.created_at.desc()).all()
    panels = [panel.__dict__ for panel in panels]
    for panel in panels:
        panel["published_by"] = User.query.get(panel["created_by"]).name
        panel["records"] = []
        for id in panel["lab_ids"].split(","):
            panel["records"].append(get_row(data, id))
    return render_template('panels.html', name=current_user.name,
                           root_url=request.url_root,
                           panels=panels, modification_access=True,
                           page_title="My Panels")


@main.route('/panel')
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
        if current_user.is_authenticated:
            current_user_id = current_user.id
            if current_user_id == panel["created_by"]:
                return render_template('panel.html',
                                       panel=panel,
                                       root_url=request.url_root,
                                       modification_access=True,
                                       page_title="Panel")
        if panel["is_publish"] == False or panel["is_publish"] == None:
            flash(f"Panel {panel_id} is not publicly available.", "warning")
            if current_user.is_authenticated:
                return redirect(url_for('main.show_panels'))
            else:
                return redirect(url_for('main.index'))
        return render_template('panel.html',
                               panel=panel, root_url=request.url_root,
                               page_title="Panel")
    flash(f"No panel found with id {panel_id}", "warning")
    return redirect(url_for('main.index'))


@main.route('/add', methods=["GET", "POST"])
@login_required
def add_panel():
    antibodies, conjugates, antibody_mapper = get_antibody_conjugate_mapper()
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
                                       conjugates=conjugates,
                                       page_title="Add Panel")
            elif "secondary_form" in request.form:
                lab_ids = request.form.getlist("selected_lab_ids")
                panel_title = request.form.get("panel_title")
                is_publish_value = request.form.get("is_publish", False)
                created_by = current_user.id
                lab_ids = ",".join(lab_ids)
                is_publish = False
                if is_publish_value == "public":
                    is_publish = True
                new_panel = Panel(title=panel_title,
                                  created_by=created_by,
                                  lab_ids=lab_ids,
                                  is_publish=is_publish)
                db.session.add(new_panel)
                db.session.commit()
                flash('New panel created.', 'success')
                return redirect(f'panel?id={new_panel.id}')
        except Exception as ex:
            flash(str(ex), "error")
            return redirect(url_for("main.add_panel"))
    else:
        return render_template('add.html',
                               name=current_user.name,
                               antibodies=antibodies,
                               conjugates=conjugates,
                               antibody_mapper=json.dumps(antibody_mapper),
                               page_title="Add Panel")


@main.route('/delete', methods=["POST"])
@login_required
def delete_panel():
    try:
        current_user_id = current_user.id
        panel_id = request.form.get("panel_id")
        panel = Panel.query.get(panel_id)
        if panel:
            if current_user_id == panel.created_by:
                db.session.delete(panel)
                db.session.commit()
                flash(f'Panel <b>{panel.title}</b> is deleted successfully.',
                      'success')
                return redirect(url_for("main.show_my_panels"))
            else:
                flash(f'You are not authorized to delete this panel.', 'error')
                return redirect(url_for("main.show_my_panels"))
        else:
            flash(f'Panel with id {panel_id} is not found.', 'error')
            return redirect(url_for("main.show_my_panels"))
    except Exception as ex:
        flash(str(ex), "error")
        return redirect(url_for("main.show_my_panels"))


@main.route('/change_visibility', methods=["POST"])
@login_required
def change_visibility():
    try:
        current_user_id = current_user.id
        panel_id = request.form.get("panel_id")
        panel = Panel.query.get(panel_id)
        if panel:
            if current_user_id == panel.created_by:
                current_visibility = panel.is_publish
                if current_visibility == True:
                    panel.is_publish = False
                else:
                    panel.is_publish = True
                db.session.commit()
                flash(f'Panel <b>{panel.title}</b> is updated successfully.',
                      'success')
                return redirect(f'panel?id={panel.id}')
            else:
                flash(f'You are not authorized to modify this panel.', 'error')
                return redirect(url_for("main.show_my_panels"))
        else:
            flash(f'Panel with id {panel_id} is not found.', 'error')
            return redirect(url_for("main.show_my_panels"))
    except Exception as ex:
        flash(str(ex), "error")
        return redirect(url_for("main.show_my_panels"))
