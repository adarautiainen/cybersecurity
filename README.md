# Cyber Security Base / Project 1

This project is done for University of Helsinki course Cyber Security Base.

## How to use this app

1. Clone the project

2.
```bash
~cybersecurity/$ cd project1
```
3.
```bash
poetry install
poetry shell
```
4.
```bash
python manage.py makemigrations
```
5.
```bash
python manage.py migrate
```
6. Start the app
```bash
python manage.py runserver
```

## Project report

**FLAW 1: Injection**

Link to the flaw: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L65 and more specific this line: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L76

Description of flaw: According to OWASP app is vulnerable to attack if data given by user is not validated and dynamic queries are used directly. In views.py ‘take_notes’ SQL query is used which uses user input that isn’t validated. This makes the app vulnerable to SQL injections, because user could input commands that for example can delete or manipulate data in database. 

Link to the fix: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L87

Description of fix: The fix uses Django’s built-in forms, in the code ‘NoteForm’ is used that handles data validation and saving. This is safer than extracting the data from request and making SQL queries. 

**FLAW 2: Broken access control**

Link to the flaw: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L128

Description of flaw: According to OWASP it is common vulnerability that access should be for specific users, but is available to anyone. In ‘view_notes’ function gets all notes from database using ‘Note.objects.all’ and shows the notes made by all users, when actually users should only see their own notes. 

Link to the fix: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L136

Description of fix: In the commented out part users can only see the notes they have made. This is done by filtering ‘Note.objects.filter(user=request.user)’, doing this unauthorized access to others information isn’t possible.

**FLAW 3: Identification and authentication failures**

Link to the flaw: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L23

Description of flaw: According to OWASP app can have authentication weakness if it permits well-known or weak passwords. In ‘login_view’ users passwords aren’t validated, so users can use weak passwords, which isn’t safe because hackers can guess easily the passwords and get users information. Note that part of this flaw is also in settings.py: https://github.com/adarautiainen/cybersecurity/blob/main/project1/project1/settings.py#L95 where the password validators are commented out.

Link to the fix: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L41 and take comments off in https://github.com/adarautiainen/cybersecurity/blob/main/project1/project1/settings.py#L95

Description of fix: In the fix Django’s password validators are used, which prevent the use of weak password, so users are more safe. Using the fix if user tries to login with weak password it gives error message and user can’t login.

**FLAW 4: Security misconfiguration**

Link to the flaw: https://github.com/adarautiainen/cybersecurity/blob/main/project1/project1/settings.py#L28

Description of flaw: According to OWASP app may be vulnerable if there are unnecessary ports enabled or security settings in the application framework are not set to secure values. In settings.py ‘ALLOWED_HOSTS’ is configured to accept requests from all hosts using wildcard value ‘*’. Allowing requests from all hosts can lead to cross-site request forgery and cross-site scripting attacks and also unauthorized access.

Link to the fix: https://github.com/adarautiainen/cybersecurity/blob/main/project1/project1/settings.py#L32

Description of fix: In the fix only localhost is allowed as a host, there could be added other hosts that are known to be safe. This reduces the attack risk and unauthorized access.

**FLAW 5: Server-side request forgery**

Link to the flaw: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L67

Description of flaw: According to OWASP server side request forgery flaws occurs if app fetches remote resource without validating URL that is given by user. In ‘take_notes’ the URL from user input is retrieved without validation and URL is used in ‘requests.get()’. Because of this an attacker could make SSRF attack, where the server is manipulated to make unintended requests. 

Link to the fix: https://github.com/adarautiainen/cybersecurity/blob/main/project1/app/views.py#L87

Description of fix: In the fix the URL from user input is validated and before using ‘request.get()’ it is checked that the URL is in trusted domains. In the ‘is_safe_url’ is now only two trusted domains, but this function could be modified, I just made it as simple as possible. This fix reduces the risk of the attacks. 
