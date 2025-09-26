# This is boiler template for production ready django template with best practice
# created by Selim Reza (selim.reza.uits@gmail.com)

<!-- First -->
### created venv
### requirements.txt list:
asgiref==3.8.1
backports-zoneinfo==0.2.1
django==4.2.23
django-cors-headers==4.4.0
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
isort==5.13.2
pygments==2.19.1
pyjwt==2.9.0
python-dotenv==1.0.1
sqlparse==0.5.3
typing-extensions==4.13.2
whitenoise==6.7.0


<!-- Installed -->
Django
Django Rest Framework
SimpleJWT
<!-- extra pakages -->
Django-hijack : Admins can log in and work on behalf of other users without having to know their credentials.
::: installed and added to installed app and middleware but haven't used yet.
django-admin-sortable2 : Generic drag-and-drop ordering for objects in the Django admin interface.
::: installed and added to installed app but haven't used yet.
django-admin-env-notice: 














# Next to do:

| Goal              | Suggestion                                                          |
| ----------------- | ------------------------------------------------------------------- |
| 🐳 Dockerize it?  | Add `Dockerfile`, `docker-compose.yml`, and `traefik.yml` if needed |
| 🔒 HTTPS & SSL    | Set up Let’s Encrypt or Cloudflare with Nginx                       |
| 🌐 Public Hosting | Deploy on DigitalOcean, Railway, Fly.io, or Render                  |
| 📈 Monitoring     | Add Sentry or Rollbar, Prometheus + Grafana (optional)              |
| 🧪 CI/CD          | GitHub Actions for test/lint/black/mypy on push                     |
