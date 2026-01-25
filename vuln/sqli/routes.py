import re
import time

from flask import redirect, render_template, request, url_for

from db import get_db, init_db

TITLES = [
    "Authentication Module",
    "Data Lookup",
    "Data Retrieval",
    "System Diagnostics",
    "Access Control",
    "Performance Monitor",
    "Input Validation",
    "Multi-Step Process",
    "Security Layer",
    "Batch Operations",
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
        db = get_db()
        c = db.cursor()
        c.executescript("DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS secrets;")
        init_db(db)
        return redirect("/")

    @app.route("/level1", methods=["GET", "POST"])
    def level1():
        query_log = None
        msg = ""
        if request.method == "POST":
            username = request.form.get("username", "")
            password = request.form.get("password", "")
            sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            query_log = sql
            try:
                cur = get_db().cursor()
                cur.execute(sql)
                if cur.fetchone():
                    msg = (
                        "<div class='text-green-400 text-2xl font-bold'>ACCESS GRANTED</div>"
                        "<div class='mt-4 p-4 border-2 border-green-500 bg-green-900/30 text-green-400 font-bold text-xl animate-pulse'>"
                        " CONGRATULATIONS! SQL Injection successful! </div>"
                    )
                else:
                    msg = "<div class='text-red-500 font-bold'>ACCESS DENIED</div>"
            except Exception as e:
                error_str = str(e)
                if "unrecognized token" in error_str.lower():
                    msg = "<div class='text-red-500 font-bold'>ACCESS DENIED</div>"
                else:
                    msg = f"<div class='text-red-500'>SYSTEM ERROR: {e}</div>"

        return render_page(1, "Authentication system active.", "level1.html", msg=msg)

    @app.route("/level2")
    def level2():
        id_param = request.args.get("id", "1")
        sql = f"SELECT name, price FROM products WHERE id = {id_param}"
        try:
            cur = get_db().cursor()
            cur.execute(sql)
            items = cur.fetchall()
        except Exception:
            items = []

        show_congrats = len(items) > 1

        return render_page(
            2,
            "Data lookup system active.",
            "level2.html",
            items=items,
            id_param=id_param,
            show_congrats=show_congrats,
        )

    @app.route("/level3")
    def level3():
        search = request.args.get("search", "")
        results = []
        sql = f"SELECT name, description, price FROM products WHERE name LIKE '%{search}%'"
        if search:
            try:
                cur = get_db().cursor()
                cur.execute(sql)
                results = cur.fetchall()
            except Exception as e:
                error_str = str(e)
                if "unrecognized token" in error_str.lower():
                    results = []
                else:
                    results = [("System Error", str(e), 0)]

        show_flag_congrats = any("FLAG" in str(result[1]) or "FLAG" in str(result[0]) for result in results)

        return render_page(
            3,
            "Data retrieval system active.",
            "level3.html",
            results=results,
            search=search,
            show_flag_congrats=show_flag_congrats,
        )

    @app.route("/level4")
    def level4():
        id_param = request.args.get("uuid", "user-001")
        error_msg = None
        success_signal = False

        sql = f"SELECT * FROM users WHERE username = '{id_param}'"

        try:
            cur = get_db().cursor()
            cur.execute(sql)
            cur.fetchall()
        except Exception as e:
            error_msg = str(e)
            if (
                "unrecognized token" in error_msg
                or "syntax" in error_msg.lower()
                or "unterminated" in error_msg.lower()
            ):
                success_signal = True

        return render_page(
            4,
            "System diagnostics active.",
            "level4.html",
            id_param=id_param,
            error_msg=error_msg,
            success_signal=success_signal,
        )

    @app.route("/level5")
    def level5():
        username = request.args.get("u", "")

        if username.strip() == "admin":
            status = "<span class='text-red-500 font-bold'>[ ACCESS BLOCKED ]</span>"
            sql = "BLOCKED: Direct access not allowed."
        else:
            sql = f"SELECT * FROM users WHERE username = '{username}'"
            exists = False
            try:
                cur = get_db().cursor()
                cur.execute(sql)
                if cur.fetchone():
                    exists = True
            except Exception:
                pass

            status = (
                "<span class='text-green-400 font-bold'>[ USER FOUND ]</span>"
                if exists
                else "<span class='text-slate-500'>[ NOT FOUND ]</span>"
            )
            if exists and username.strip() != "admin":
                status += (
                    "<div class='mt-4 p-3 border-2 border-green-500 bg-green-900/30 text-green-400 font-bold text-lg animate-pulse'>"
                    " CONGRATULATIONS! SQL Injection successful! </div>"
                )

        return render_page(5, "Access control system active.", "level5.html", username=username, status=status)

    @app.route("/level6")
    def level6():
        search = request.args.get("q", "")
        start_time = time.time()
        results = []

        if search:
            sql = f"SELECT * FROM products WHERE name = '{search}'"
            try:
                cur = get_db().cursor()
                cur.execute(sql)
                results = cur.fetchall()
            except Exception:
                pass

        duration = time.time() - start_time
        msg = f"{duration:.2f}s" if duration > 0.1 else "0.00s"

        status_class = "text-green-500 font-bold border-green-500" if duration > 2 else "text-slate-600 border-slate-800"

        return render_page(
            6,
            "Performance monitor active.",
            "level6.html",
            search=search,
            msg=msg,
            status_class=status_class,
            duration=duration,
        )

    @app.route("/level7")
    def level7():
        id_param = request.args.get("id", "1")
        item = None
        error = None

        if " " in id_param:
            error = "SECURITY ERROR: Invalid input detected."
            sql = "BLOCKED"
        else:
            sql = f"SELECT name, price, description FROM products WHERE id = {id_param}"
            try:
                cur = get_db().cursor()
                cur.execute(sql)
                row = cur.fetchone()
                if row:
                    item = dict(row)
            except Exception as e:
                error_str = str(e)
                if "unrecognized token" in error_str.lower():
                    error = None
                else:
                    error = f"System Error: {str(e)}"

        return render_page(
            7,
            "Input validation system active.",
            "level7.html",
            id_param=id_param,
            item=item,
            error=error,
        )

    @app.route("/level8", methods=["GET", "POST"])
    def level8():
        if request.method == "POST":
            username = request.form.get("username", "")
            if username.strip() == "admin":
                return render_page(
                    8,
                    "Multi-step process.",
                    "level8.html",
                    step="register",
                    error_msg="ERROR: User 'admin' already exists.",
                )
            return redirect(url_for("level8", step="view", user=username))

        step = request.args.get("step", "register")
        stored_user = request.args.get("user", "")

        if step == "register":
            return render_page(8, "User registration system active.", "level8.html", step="register")

        sql = f"SELECT role FROM users WHERE username = '{stored_user}'"
        role = "guest"
        try:
            cur = get_db().cursor()
            cur.execute(sql)
            res = cur.fetchone()
            if res:
                role = res[0]
        except Exception as e:
            error_str = str(e)
            if "unrecognized token" in error_str.lower():
                role = "guest"
            else:
                role = f"ERROR: {e}"

        return render_page(
            8,
            "User profile display active.",
            "level8.html",
            step="view",
            user=stored_user,
            role=role,
        )

    @app.route("/level9")
    def level9():
        search = request.args.get("q", "")
        results = []

        if re.search(r"union\s+select", search, re.IGNORECASE):
            msg = (
                "<div class='text-red-500 text-center text-3xl font-bold p-8 border-2 border-red-500 bg-red-900/30'>"
                "SECURITY BLOCKED: Invalid query pattern</div>"
            )
            return render_page(9, "Security layer active.", "level9.html", blocked_msg=msg)

        sql = f"SELECT name, description, price FROM products WHERE name LIKE '%{search}%'"
        try:
            cur = get_db().cursor()
            cur.execute(sql)
            results = cur.fetchall()
        except Exception:
            results = []

        show_flag_congrats = any("FLAG" in str(result[1]) or "FLAG" in str(result[0]) for result in results)

        return render_page(
            9,
            "Advanced filtering active.",
            "level9.html",
            search=search,
            results=results,
            show_flag_congrats=show_flag_congrats,
        )

    @app.route("/level10", methods=["GET", "POST"])
    def level10():
        msg = ""
        query_log = ""
        if request.method == "POST":
            user_input = request.form.get("id", "")
            sql = f"SELECT * FROM users WHERE id = {user_input}"
            query_log = sql
            try:
                cur = get_db().cursor()
                cur.executescript(sql)
                cur.execute("SELECT password FROM users WHERE username='admin'")
                if cur.fetchone()[0] == "pwned":
                    msg = (
                        "<div class='text-green-400 text-2xl font-bold'>SYSTEM MODIFIED! Configuration changed.</div>"
                        "<div class='mt-4 p-4 border-2 border-green-500 bg-green-900/30 text-green-400 font-bold text-xl animate-pulse'>"
                        " CONGRATULATIONS! Blind SQL Injection with system modification successful! </div>"
                    )
                else:
                    msg = "<div class='text-slate-400 italic'>Operation executed. System unchanged.</div>"
            except Exception as e:
                error_str = str(e)
                if "unrecognized token" in error_str.lower():
                    msg = "<div class='text-slate-400 italic'>Operation executed. System unchanged.</div>"
                else:
                    msg = f"<div class='text-red-500'>Error: {e}</div>"

        return render_page(10, "Batch operations active.", "level10.html", msg=msg)
