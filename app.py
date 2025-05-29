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
    return render_template("index.html")


@app.route("/s")
def search():
    args = request.args.get("q")
    if args:
        search_query = args.strip()
        conn = get_db_connection()
        all_tests = conn.execute(
            """SELECT t.*, l.docbase_link, l.source_link
               FROM tests t 
               LEFT JOIN (
                   SELECT test_id, docbase_link, source_link
                   FROM (
                       SELECT test_id, docbase_link, source_link, votes, date_added,
                              ROW_NUMBER() OVER (PARTITION BY test_id ORDER BY votes DESC, date_added ASC) as rn
                       FROM links
                   ) ranked
                   WHERE rn = 1
               ) l ON t.id = l.test_id""",
        ).fetchall()
        conn.close()

        scored_tests = []
        for test in all_tests:
            name_score = fuzz.token_set_ratio(
                search_query.lower(), test["name"].lower()
            )
            abbrev_score = (
                fuzz.ratio(search_query.lower(), test["abbreviation"].lower())
                if test["abbreviation"]
                else 0
            )
            best_score = max(name_score, abbrev_score)
            if best_score > 50:
                scored_tests.append((test, best_score))

        scored_tests.sort(key=lambda x: x[1], reverse=True)
        tests = [test for test, _ in scored_tests]
    else:
        tests = []
    return render_template("search.html", tests=tests)


@app.route("/b")
def browse():
    conn = get_db_connection()
    tests = conn.execute(
        """SELECT t.*, l.docbase_link, l.source_link 
           FROM tests t 
           LEFT JOIN (
               SELECT test_id, docbase_link, source_link
               FROM (
                   SELECT test_id, docbase_link, source_link, votes, date_added,
                          ROW_NUMBER() OVER (PARTITION BY test_id ORDER BY votes DESC, date_added ASC) as rn
                   FROM links
               ) ranked
               WHERE rn = 1
           ) l ON t.id = l.test_id 
           ORDER BY t.name""",
    ).fetchall()
    conn.close()
    return render_template("browse.html", tests=tests)


@app.route("/<int:id>")
def show_detail(id):
    if id <= 0:
        return "Invalid ID", 400

    referrer = request.args.get("from", "")
    conn = get_db_connection()
    test = conn.execute(
        "SELECT * FROM tests WHERE id = ?",
        (id,),
    ).fetchone()

    if test is None:
        return "Test not found", 404

    links = conn.execute(
        "SELECT * FROM links WHERE test_id = ?",
        (id,),
    ).fetchall()

    conn.close()
    return render_template("detail.html", test=test, links=links, referrer=referrer)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
