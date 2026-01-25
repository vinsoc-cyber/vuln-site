import html
import json
import re
import urllib.parse

from flask import redirect, render_template, request

import db

TITLES = [
    "Data Processing",
    "Message Storage",
    "URL Handler",
    "Content Filter",
    "Profile Manager",
    "Link Validator",
    "System Monitor",
    "Security Scanner",
    "Template Engine",
    "API Dashboard",
]


def render_page(level_id, description, template_name, **kwargs):
    return render_template(
        template_name,
        active_level=level_id,
        titles=TITLES,
        current_title=TITLES[level_id - 1],
        description=description,
        **kwargs,
    )


def register_routes(app):
    @app.route("/")
    def index():
        return redirect("/level1")

    @app.route("/reset")
    def reset():
        db.reset_db()
        return redirect("/")

    @app.route("/level1")
    def level1():
        query = request.args.get("q", "")
        return render_page(1, "Search functionality active.", "level1.html", query=query)

    @app.route("/level2", methods=["GET", "POST"])
    def level2():
        if request.method == "POST":
            comment = request.form.get("comment", "")
            conn = db.get_db()
            c = conn.cursor()
            c.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
            conn.commit()
            return redirect("/level2")

        conn = db.get_db()
        c = conn.cursor()
        c.execute("SELECT content FROM comments")
        comments = c.fetchall()

        return render_page(2, "Message storage system active.", "level2.html", comments=comments)

    @app.route("/level3")
    def level3():
        return render_page(3, "URL parameter processing active.", "level3.html")

    @app.route("/level4")
    def level4():
        query = request.args.get("q", "")
        safe_query = re.sub(r"(?i)<script.*?>.*?</script>", "[FILTERED]", query)
        safe_query = re.sub(r"(?i)<script", "[FILTERED]", safe_query)

        return render_page(4, "Content filtering system active.", "level4.html", query=query, safe_query=safe_query)

    @app.route("/level5")
    def level5():
        username = request.args.get("u", "User")
        safe_username = username.replace("<", "&lt;").replace(">", "&gt;")

        return render_page(5, "Profile management active.", "level5.html", safe_username=safe_username)

    @app.route("/level6")
    def level6():
        link = request.args.get("link", "https://example.com")
        safe_link = html.escape(link)

        return render_page(6, "Link validation system active.", "level6.html", safe_link=safe_link)

    @app.route("/level7")
    def level7():
        payload = request.args.get("p", "System Normal")
        safe_payload = payload.replace("<", "").replace(">", "").replace('"', "").replace("/", "")

        return render_page(7, "System monitoring active.", "level7.html", safe_payload=safe_payload)

    @app.route("/level8")
    def level8():
        raw_query = (
            request.query_string.decode("utf-8").split("=")[1]
            if "=" in request.query_string.decode("utf-8")
            else ""
        )

        decoded_once = urllib.parse.unquote(raw_query)

        if "<script" in decoded_once.lower() or "javascript:" in decoded_once.lower():
            blocked_msg = (
                "<div class='text-red-500 text-center text-4xl font-bold border-2 border-red-500 p-10 bg-red-900/20'>"
                "🚫 REQUEST BLOCKED</div>"
            )
            return render_page(8, "BLOCKED", "level8.html", blocked_msg=blocked_msg)

        final_content = urllib.parse.unquote(decoded_once)

        return render_page(8, "Security scanner active.", "level8.html", final_content=final_content)

    @app.route("/level9")
    def level9():
        return render_page(9, "Template processing active.", "level9.html")

    @app.route("/api/widgets")
    def api_widgets():
        callback = request.args.get("callback", "init")
        data = json.dumps({"status": "ok", "items": ["Widget A", "Widget B"]})
        return f"{callback}({data})"

    @app.route("/level10")
    def level10():
        query = request.args.get("q", "Active")
        return render_page(10, "API dashboard active.", "level10.html", query=query)
