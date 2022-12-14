# Courses
A microservice manages Course project definitions, descriptions and teams.

## Functionalities and APIs

### Create
- ```/api/sections/new_section```
- ```/api/sections/<call_no>/new_student```
- ```/api/sections/<call_no>/new_project```
- ```/api/sections/<call_no>/projects/<project_id>/new_student```
- ```/api/sections/<call_no>/projects/<project_id>/new_students```

### Read
- ```/api/sections```
- ```/api/sections/students```
- ```/api/sections/<call_no>```
- ```/api/sections/<call_no>/students```
- ```/api/sections/<call_no>/students/no_project```
- ```/api/sections/<call_no>/projects```
- ```/api/sections/all_projects```
- ```/api/sections/<call_no>/projects/<project_id>```
- ```/api/sections/<call_no>/projects/<project_id>/all_students```
- ```/api/sections/<call_no>/students/<uni>```

### Update
- ```/api/enrollment/<uni>```
- ```/api/sections/<call_no>/update_project/<project_id>```
- ```/api/sections/<call_no>```

### Delete
- ```/api/sections/<call_no>/students/<uni>```
- ```/api/sections/delete_project/<project_id>```
- ```/api/sections/<call_no>```

## Running unit tests