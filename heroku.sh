#!/bin/sh

heroku login

heroku container:login

heroku container:push web -a menu-semanal-v2

heroku container:release web -a menu-semanal-v2

xdg-open https://menu-semanal-v2.herokuapp.com/api/
