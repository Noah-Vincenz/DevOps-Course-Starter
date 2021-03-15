echo $HEROKU_API_KEY | docker login --username $USERNAME --password-stdin registry.heroku.com
docker tag $USERNAME/todo-app:latest registry.heroku.com/devops-project-exercise-8/web
docker push registry.heroku.com/devops-project-exercise-8/web
heroku git:remote -a devops-project-exercise-8
heroku container:release web