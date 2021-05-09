# eMenu
This is a project built for recruitment purposes.
It's goal is to build an app on Django Rest Framework to manage menus and to send periodic email with news.

Project contains database with dummy data for testing purposes.

## Instruction
In order to run application and check its functionality please follow below steps:
1. Run Docker (Docker Desktop for windows)
2. Run start.sh file.
3. Open http://127.0.0.1:8000/docs to check out application functionality.

### Test coverage
Open htmlcov/index.html in your browser, to see a coverage report.

### API
Api functionality is divided on public and nonpublic, which require to being logged in.
For testing purposes use admin account by logging on http://127.0.0.1:8000/admin with below credentials:

username: admin
password: admin

### Closing application
Remember to close application by running below command in Command Prompt:
```
$ docker-compose down
```
