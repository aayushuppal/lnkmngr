from flask import current_app as app
from flask import render_template, request, redirect
from utils.db import get_table_categories
from utils import under_str_frmt, is_valid_category_id
from utils.db import (
    get_all_link_tables,
    add_new_table,
    add_new_entry,
    del_entry,
)
from utils.tree import get_links_json_as_list
from utils.consts import CATEGORY_TYPE, LINK_TYPE
import json


@app.route("/", methods=["GET"])
def home():
    title = "lnkmngr"
    link_tables = get_all_link_tables()
    return render_template("lnkmngr_list.jinja2", title=title, link_tables=link_tables)


@app.route("/add_link_table_route/", methods=["POST"])
def add_link_table_route():
    rf = request.form
    table_name = rf["new_table_name"].strip()
    if table_name:
        add_new_table(table_name)
    return redirect("/")


@app.route("/<table_name>/", methods=["GET"])
def render_list_page_route(table_name):
    title = f"lnkmngr - {under_str_frmt(table_name)}"
    links_json = get_links_json_as_list(table_name)
    all_cats, cat_map = get_table_categories(table_name)
    return render_template(
        "lnkmngr_tree_view.jinja2",
        title=title,
        table_name=table_name,
        links_json=links_json,
        all_cats=all_cats,
        cat_map=cat_map,
    )


@app.route("/add_new_entry_route/", methods=["POST"])
def add_new_entry_route():
    rj = request.get_json()
    table_name = request.get_json()["table_name"]
    new_entry_cat_id = None

    if rj["cat_1_id"] != "":
        if is_valid_category_id(rj["cat_1_id"]):
            cat_1_id = int(rj["cat_1_id"])
        else:
            cat_label = rj["cat_1_val"].strip()
            assert cat_label != ""
            cat_1_id = add_new_entry(
                table_name=table_name,
                label=cat_label,
                type=CATEGORY_TYPE,
                parent_id=None,
                href=None,
            )
        new_entry_cat_id = cat_1_id

    if rj["cat_2_id"] != "":
        if is_valid_category_id(rj["cat_2_id"]):
            cat_2_id = int(rj["cat_2_id"])
        else:
            cat_label = rj["cat_2_val"].strip()
            assert cat_label != ""
            assert cat_1_id is not None
            cat_2_id = add_new_entry(
                table_name=table_name,
                label=cat_label,
                type=CATEGORY_TYPE,
                parent_id=cat_1_id,
                href=None,
            )
        new_entry_cat_id = cat_2_id

    ent_label = rj["label"].strip()
    if ent_label != "":
        ent_href = rj["href"].strip()
        add_new_entry(
            table_name=table_name,
            label=ent_label,
            type=LINK_TYPE,
            parent_id=new_entry_cat_id,
            href=ent_href,
        )

    return app.response_class(
        response=json.dumps({}), status=200, mimetype="application/json"
    )


@app.route("/del_entries_route/", methods=["POST"])
def del_entries_route():
    table_name = request.get_json()["table_name"]
    for id in request.get_json()["ids"]:
        del_entry(table_name, int(id))

    return app.response_class(
        response=json.dumps({}), status=200, mimetype="application/json"
    )
