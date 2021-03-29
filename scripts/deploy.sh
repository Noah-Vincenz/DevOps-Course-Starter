echo $HEROKU_API_KEY | docker login --username $USERNAME --password-stdin registry.heroku.com
APP_NAME="devops-project-exercise-8"
docker tag $USERNAME/todo-app:latest registry.heroku.com/$APP_NAME/web
docker push registry.heroku.com/$APP_NAME/web
heroku container:release web -a $APP_NAME