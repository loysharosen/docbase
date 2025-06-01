import sqlite3
from flask import Flask, request, render_template
from rapidfuzz import fuzz

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("docbase.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    conn = get_db_connection()
    count_docs = conn.execute(
        """SELECT COUNT(*) AS count FROM docs""",
    ).fetchone()
    conn.close()
    return render_template("index.html", count_docs=count_docs)


@app.route("/s")
def search():
    args = request.args.get("q")
    if args:
        search_query = args.strip()
        conn = get_db_connection()
        all_docs = conn.execute(
            """SELECT t.*, l.docbase_link, l.source_link,
                      (SELECT COUNT(*) FROM links WHERE doc_id = t.id) as link_count
               FROM docs t 
               LEFT JOIN (
                   SELECT doc_id, docbase_link, source_link
                   FROM (
                       SELECT doc_id, docbase_link, source_link, votes, date_added,
                              ROW_NUMBER() OVER (PARTITION BY doc_id ORDER BY votes DESC, date_added ASC) as rn
                       FROM links
                   ) ranked
                   WHERE rn = 1
               ) l ON t.id = l.doc_id""",
        ).fetchall()
        conn.close()

        scored_docs = []
        for doc in all_docs:
            name_score = fuzz.token_set_ratio(search_query.lower(), doc["name"].lower())
            abbrev_score = (
                fuzz.ratio(search_query.lower(), doc["abbreviation"].lower())
                if doc["abbreviation"]
                else 0
            )
            best_score = max(name_score, abbrev_score)
            if best_score > 49:
                scored_docs.append((doc, best_score))

        scored_docs.sort(key=lambda x: x[1], reverse=True)
        docs = [doc for doc, _ in scored_docs]
    else:
        docs = []
    return render_template("search.html", docs=docs)


@app.route("/b")
def browse():
    conn = get_db_connection()
    docs = conn.execute(
        """SELECT d.*, 
                  GROUP_CONCAT(l.docbase_link) as docbase_links,
                  GROUP_CONCAT(l.source_link) as source_links,
                  (SELECT COUNT(*) FROM links WHERE doc_id = d.id) as link_count
            FROM docs d
            LEFT JOIN links l ON d.id = l.doc_id
            GROUP BY d.id, d.name, d.abbreviation, d.description, d.keywords
            ORDER BY d.name""",
    ).fetchall()
    conn.close()
    return render_template("browse.html", docs=docs)


@app.route("/<int:id>")
def show_detail(id):
    if id <= 0:
        return "Invalid ID", 400

    referrer = request.args.get("from", "")
    conn = get_db_connection()
    doc = conn.execute(
        "SELECT * FROM docs WHERE id = ?",
        (id,),
    ).fetchone()

    if doc is None:
        return "doc not found", 404

    links = conn.execute(
        "SELECT * FROM links WHERE doc_id = ?",
        (id,),
    ).fetchall()

    conn.close()
    return render_template("detail.html", doc=doc, links=links, referrer=referrer)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
