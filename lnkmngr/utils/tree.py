from utils.db import read_table, update_entry_parent


def get_links_json_as_map(table_name):
    df = read_table(table_name)
    node_map = {}
    for id, row in df.iterrows():
        if row.type == "category":
            node_map[str(id)] = {
                "id": str(id),
                "type": row.type,
                "parent": "#" if row.parent_id is None else str(int(row.parent_id)),
                "text": row.label,
            }
        elif row.type == "link":
            node = {
                "id": str(id),
                "type": row.type,
                "parent": "#" if row.parent_id is None else str(int(row.parent_id)),
                "text": row.label,
            }
            if row.href:
                node["a_attr"] = {
                    "style": "text-decoration: underline; color: #0d6efd",
                    "href": row.href,
                }
            node_map[str(id)] = node
    return node_map


def reorder_tree(table_name, new_tree_node_list):
    old_tree_node_map = get_links_json_as_map(table_name)
    for node in new_tree_node_list:
        id = node["id"]
        new_parent_id = None if (node["parent"] == "#") else int(node["parent"])
        old_parent_id = (
            None
            if (old_tree_node_map[id]["parent"] == "#")
            else int(old_tree_node_map[id]["parent"])
        )
        id = int(id)

        if new_parent_id != old_parent_id:
            update_entry_parent(table_name, id, new_parent_id)
