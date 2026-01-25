import time

from flask import current_app, redirect, render_template, render_template_string, request

from db import get_db, init_db

TITLES = [
    "Variable Renderer",
    "Expression Calculator",
    "Config Injector",
    "Filter Bypass",
    "Control Injection",
    "Context Hijack",
    "Attribute Traversal",
    "Helper Exposure",
    "Stored Template",
    "Blacklist Renderer",
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
        c.executescript("DROP TABLE IF EXISTS users; DROP TABLE IF EXISTS templates;")
        init_db(db)
        return redirect("/")

    @app.route("/level1", methods=["GET", "POST"])
    def level1():
        user_input = request.form.get("template", "") if request.method == "POST" else request.args.get("template", "")
        rendered_output = ""
        success_detected = False

        if user_input:
            try:
                template = f"Hello, {user_input}!"
                rendered_output = render_template_string(template)
                if "__class__" in rendered_output or "config" in rendered_output or "/" in rendered_output:
                    success_detected = True
            except Exception as e:
                rendered_output = f"Error: {str(e)}"

        return render_page(
            1,
            "Variable rendering system active.",
            "level1.html",
            user_input=user_input,
            rendered_output=rendered_output,
            success_detected=success_detected,
        )

    @app.route("/level2")
    def level2():
        expression = request.args.get("expr", "7 * 6")
        result = ""
        success_detected = False

        if expression:
            try:
                template = f"{{{{ {expression} }}}}"
                result = render_template_string(template)
                try:
                    float_val = float(result)
                except Exception:
                    success_detected = True
            except Exception as e:
                result = f"Error: {str(e)}"

        return render_page(
            2,
            "Expression evaluation active.",
            "level2.html",
            expression=expression,
            result=result,
            success_detected=success_detected,
        )

    @app.route("/level3", methods=["GET", "POST"])
    def level3():
        config_name = request.form.get("config", "") if request.method == "POST" else request.args.get("config", "")
        rendered_output = ""
        success_detected = False

        if config_name:
            try:
                template = f"Config key: {{{{ config.{config_name} }}}}"
                rendered_output = render_template_string(template)
                if any(key in rendered_output.lower() for key in ["secret", "env", "key", "password"]):
                    success_detected = True
            except Exception as e:
                rendered_output = f"Error: {str(e)}"

        return render_page(
            3,
            "Config injection system active.",
            "level3.html",
            config_name=config_name,
            rendered_output=rendered_output,
            success_detected=success_detected,
        )

    @app.route("/level4")
    def level4():
        name = request.args.get("name", "Guest")
        formatted_name = name
        success_detected = False

        try:
            blocked_patterns = ["__class__", "__base__", "__mro__", "__subclasses__", "config", "self"]
            is_blocked = any(pattern in name for pattern in blocked_patterns)

            if not is_blocked:
                template = f"{{{{ {name} }}}}"
                formatted_name = render_template_string(template)
                if formatted_name != name and len(formatted_name) > 50:
                    success_detected = True
            else:
                formatted_name = "[BLOCKED] Input contains restricted patterns"
        except Exception as e:
            formatted_name = f"Error: {str(e)}"

        return render_page(
            4,
            "Filter bypass active.",
            "level4.html",
            name=name,
            formatted_name=formatted_name,
            success_detected=success_detected,
        )

    @app.route("/level5", methods=["GET", "POST"])
    def level5():
        items_input = request.form.get("items", "") if request.method == "POST" else request.args.get("items", "")
        snippet = request.form.get("snippet", "") if request.method == "POST" else request.args.get("snippet", "")
        rendered_list = ""
        success_detected = False

        if items_input:
            try:
                items = [item.strip() for item in items_input.split(",")]
                template = f"""{{% for item in items %}}{{{{ item }}}} {snippet} {{% endfor %}}"""
                rendered_list = render_template_string(template, items=items)
                if any(tag in snippet for tag in ["{{", "{%"]):
                    success_detected = True
            except Exception as e:
                rendered_list = f"Error: {str(e)}"

        return render_page(
            5,
            "Control injection active.",
            "level5.html",
            items_input=items_input,
            snippet=snippet,
            rendered_list=rendered_list,
            success_detected=success_detected,
        )

    @app.route("/level6")
    def level6():
        greeting_type = request.args.get("type", "user")
        username = request.args.get("user", "Guest")
        output = ""
        success_detected = False

        try:
            context = {"user": username, "time": "day", "greeting_type": greeting_type}
            template = f"""{{{{ {greeting_type} }}}}"""
            output = render_template_string(template, **context)
            if any(indicator in str(output) for indicator in ["<module", "function", "class"]):
                success_detected = True
        except Exception as e:
            output = f"Error: {str(e)}"

        return render_page(
            6,
            "Context hijack active.",
            "level6.html",
            username=username,
            greeting_type=greeting_type,
            output=output,
            success_detected=success_detected,
        )

    @app.route("/level7")
    def level7():
        profile_id = request.args.get("id", "guest")
        field = request.args.get("field", "name")
        profile_data = {
            "guest": {"name": "Guest User", "role": "visitor", "level": 1},
            "user": {"name": "Regular User", "role": "member", "level": 5},
            "admin": {"name": "Administrator", "role": "admin", "level": 10},
        }

        display_html = ""
        success_detected = False

        try:
            profile = profile_data.get(profile_id, profile_data["guest"])
            card_template = """
            <div class="bg-slate-900 p-6 rounded-lg border border-red-900">
                <h3 class="text-2xl text-white font-bold mb-4">{{ profile.name }}</h3>
                <div class="space-y-2">
                    <div class="flex justify-between">
                        <span class="text-slate-400">Role:</span>
                        <span class="text-red-400">{{ profile.role }}</span>
                    </div>
                    <div class="flex justify-between">
                        <span class="text-slate-400">Level:</span>
                        <span class="text-red-400">{{ profile.level }}</span>
                    </div>
                </div>
            </div>
            """
            field_template = f"{{{{ profile.{field} }}}}"
            field_value = render_template_string(field_template, profile=profile)

            display_html = render_template_string(card_template, profile=profile)
            display_html += (
                "<div class='mt-4 bg-black/40 border border-red-900 p-4 text-white font-mono'>"
                f"Field Output: {field_value}</div>"
            )
            if any(indicator in str(field_value) for indicator in ["<class", "mro", "function", "object"]):
                success_detected = True
        except Exception as e:
            display_html = f"<div class='text-red-400'>Error: {str(e)}</div>"

        return render_page(
            7,
            "Attribute traversal active.",
            "level7.html",
            profile_id=profile_id,
            field=field,
            display_html=display_html,
            success_detected=success_detected,
        )

    @app.route("/level8", methods=["GET", "POST"])
    def level8():
        template_code = request.form.get("template", "") if request.method == "POST" else request.args.get("template", "")
        rendered_output = ""
        success_detected = False

        def helper(msg):
            return f"[{msg}]"

        context_vars = {
            "title": "Welcome",
            "user": "Guest",
            "items": ["a", "b", "c"],
            "count": 3,
            "helper": helper,
        }

        if template_code:
            try:
                dangerous = ["__import__", "open(", "eval", "exec", "popen"]
                if not any(d in template_code for d in dangerous):
                    rendered_output = render_template_string(template_code, **context_vars)
                    if any(
                        indicator in str(rendered_output)
                        for indicator in ["__globals__", "Flask", "request", "config", "function "]
                    ):
                        success_detected = True
                else:
                    rendered_output = "[SECURITY BLOCKED] Dangerous patterns detected"
            except Exception as e:
                rendered_output = f"Error: {str(e)}"

        return render_page(
            8,
            "Helper exposure active.",
            "level8.html",
            template_code=template_code,
            rendered_output=rendered_output,
            success_detected=success_detected,
        )

    @app.route("/level9", methods=["GET", "POST"])
    def level9():
        template_id = request.args.get("id", "")
        label = request.form.get("label", "") if request.method == "POST" else ""
        body = request.form.get("template", "") if request.method == "POST" else ""
        message = ""
        rendered_output = ""

        db = get_db()
        cur = db.cursor()

        if request.method == "POST" and body:
            label = label.strip() or "untitled"
            cur.execute("INSERT INTO templates (label, body) VALUES (?, ?)", (label, body))
            db.commit()
            message = f"Saved template #{cur.lastrowid}"

        if template_id:
            cur.execute("SELECT id, label, body FROM templates WHERE id = ?", (template_id,))
            row = cur.fetchone()
            if row:
                try:
                    rendered_output = render_template_string(
                        row["body"],
                        user="Guest",
                        now=time.strftime("%Y-%m-%d %H:%M:%S"),
                    )
                except Exception as e:
                    rendered_output = f"Error: {str(e)}"
            else:
                message = "Template not found."

        cur.execute("SELECT id, label FROM templates ORDER BY id DESC LIMIT 5")
        saved_templates = cur.fetchall()

        return render_page(
            9,
            "Stored template rendering active.",
            "level9.html",
            label=label,
            rendered_output=rendered_output,
            message=message,
            saved_templates=saved_templates,
        )

    @app.route("/level10", methods=["GET", "POST"])
    def level10():
        input_data = request.form.get("data", "") if request.method == "POST" else request.args.get("data", "")
        processed_result = ""

        if input_data:
            try:
                ctx = {"request": request, "config": current_app.config}

                blocked_patterns = [
                    "__",
                    "request",
                    "config",
                    "session",
                    "g.",
                    "url_for",
                    "import",
                    "eval",
                    "exec",
                    "popen",
                    "subprocess",
                    "os.",
                    "system",
                    "open(",
                    "read(",
                    "write(",
                ]

                is_blocked = any(pattern in input_data for pattern in blocked_patterns)
                if not is_blocked and any(ch.isdigit() for ch in input_data):
                    is_blocked = True

                if not is_blocked:
                    template_str = f"Result: {input_data}"
                    processed_result = render_template_string(template_str, ctx=ctx)
                else:
                    processed_result = "[BLOCKED] Input rejected by filter"

            except Exception as e:
                processed_result = f"Error: {str(e)}"

        return render_page(
            10,
            "Blacklist renderer active.",
            "level10.html",
            input_data=input_data,
            processed_result=processed_result,
        )
