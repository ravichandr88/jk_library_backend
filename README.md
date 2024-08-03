# Super Admin credentials
1. They are provided in .env file
2. POSTMAN-RESTAPI collection link: `https://tinyurl.com/mutp8ke4`

* First call `host/api-token-auth` with username and password to get the access token.
    * Add the token in HEADERS of the API calls with following format:
        `
        {"Authorization": "Token zszszszszszszszszszszszs"}
        `
The rest of the APIs URLs are defined in the way project description, so you can just call with respective URL.

3. Docker-Compose file: All good, except I dont have time to get complete this, with respect to Jenkins. Coz with Docker compose I am getting error that it cant find bin/bash to run python or gunicorn, when I ran migrate and then runserver, it worked perfectly. But that is not the solution for this Django project. 
command: `sudo docker-compose up -d`