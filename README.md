# FTF Django

A Django site for fuel molecule property prediction.

### Development Workflow
New features should be implemented on the `develop` branch or separate
feature branches stemming from develop. Once functional, and ideally passing
appropriate tests, feature branches can be merged into `develop` and
`develop` can be merged into `master`.

### Running Tests
Backend tests can be run with the django-admin CLI. To run tests for all apps
within the project:
```
python manage.py test
```
To run tests for a specific Django app:
```
python manage.py test {APP_NAME}
```

### Deploying Locally
To spin up a local instance of the site using Django's 
development server, run `deploy_dev.sh` from the root project directory.


### Building and Deploying Production Site 
Building and deploying the production site is handled by git post-receive hooks
following the pattern described in 
[this](https://daveceddia.com/deploy-git-repo-to-server/) 
article. Docker is used for containerization. 
Docker configurations are defined in the `Dockerfile`, `docker-compose.yml` and 
files. The build and deploy process is defined by the sequence of commands in 
`deploy_prod.sh`.
Once the production server should be set up as a git remote named `prod` a 
deployment on the production server from your local git repo can be run with:
git repository run:
```
$ git push prod
```
This will push the code to the remote server, and trigger the post-receive hook
which runs `deploy_prod.sh` on the production machine.

