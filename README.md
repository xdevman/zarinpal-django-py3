# zarinpal-django-py3
sample django zarinpal webgate with python3

**make django projet**

example:

> django-admin startproject projectname

**make app in django project:**

example:

> python manage.py startapp zarinpal

**Add variables in "Settings.py" file.**

>#SANDBOX MODE

> MERCHANT = "XXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXXXX"

> SANDBOX = True

**add "url.py" and "views.py" in your app**

**Add this path in "urls.py" project**

example : (edit "appname")

> path('appname/', include('appname.urls')),
