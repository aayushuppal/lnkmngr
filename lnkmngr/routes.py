from flask import current_app as app
from flask import render_template, request, redirect
from utils.db import get_table_categories
from utils import under_str_frmt, is_valid_category_id
from utils.db import (
    get_all_link_tables,
    add_new_table,
    add_new_entry,
    del_entry,
    drop_table,
    update_entry,
)
from utils.tree import get_links_json_as_map, reorder_tree
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


@app.route("/drop_link_table_route/", methods=["POST"])
def drop_link_table_route():
    rj = request.get_json()
    table_names = rj["table_names"]
    for table_name in table_names:
        drop_table(table_name)

    return app.response_class(
        response=json.dumps({}), status=200, mimetype="application/json"
    )


@app.route("/<table_name>/", methods=["GET"])
def render_list_page_route(table_name):
    title = f"lnkmngr - {under_str_frmt(table_name)}"
    links_json_map = get_links_json_as_map(table_name)
    all_cats, cat_map = get_table_categories(table_name)
    return render_template(
        "lnkmngr_tree_view.jinja2",
        title=title,
        table_name=table_name,
        links_json=[v for _, v in links_json_map.items()],
        all_cats=all_cats,
        cat_map=cat_map,
    )


@app.route("/add_new_entry_route/", methods=["POST"])
def add_new_entry_route():
    rj = request.get_json()
    hrefs = [x.strip() for x in rj["href"].split("\n") if x.strip()]
    table_name = rj["table_name"]
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

    if hrefs:
        if len(hrefs) == 1:
            href = hrefs[0]
            label = rj["label"].strip()
            label = label if label else href
            add_new_entry(
                table_name=table_name,
                label=label,
                type=LINK_TYPE,
                parent_id=new_entry_cat_id,
                href=href,
            )
        else:
            for href in hrefs:
                add_new_entry(
                    table_name=table_name,
                    label=href,
                    type=LINK_TYPE,
                    parent_id=new_entry_cat_id,
                    href=href,
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


@app.route("/reorder_tree_route/", methods=["POST"])
def reorder_tree_route():
    rj = request.get_json()
    table_name = rj["table_name"]
    new_tree_nodes = rj["new_tree_json"]
    reorder_tree(table_name, new_tree_nodes)

    return app.response_class(
        response=json.dumps({}), status=200, mimetype="application/json"
    )


@app.route("/edit_entry_route/", methods=["POST"])
def edit_entry_route():
    rj = request.get_json()
    table_name = rj["table_name"]
    id = int(rj["id"])

    label = rj["label"].strip()
    assert len(label) > 1

    href = rj["href"].strip()

    update_entry(table_name, id, label, href)

    return app.response_class(
        response=json.dumps({}), status=200, mimetype="application/json"
    )
