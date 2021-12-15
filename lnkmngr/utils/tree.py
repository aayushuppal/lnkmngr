from utils.db import read_table


def get_links_json_as_list(table_name):
    df = read_table(table_name)
    nodes = []
    for id, row in df.iterrows():
        if row.type == "category":
            nodes.append(
                {
                    "id": str(id),
                    "type": row.type,
                    "parent": "#" if row.parent_id is None else str(int(row.parent_id)),
                    "text": row.label,
                }
            )
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
            nodes.append(node)
    return nodes
