from utils.db import read_table


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
