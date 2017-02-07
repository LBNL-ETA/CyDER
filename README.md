# CyDER

None automatic steps before installing:
  - git pull origin master
  - docker-compose up -d
  - docker-compose exec web bash
  - mkdir logs
  - cd logs
  - touch celery_beat.log
  - touch gunicorn.log
  - ssh-keygen (3 times enter)
  - ssh-copy-id Jonathan@128.3.12.69 (host password)
  - ssh-keygen (custom naming)
  - ssh-copy-id cyder@bt-eplus.dhcp.lbl.gov  (host password)
  - python manage.py migrate cyder
  - scp init_DB file to the static repository within apps
  - python manage.py shell
  - import docker_django.apps.cyder.manual_functions as f
  - f.database_initialization()

None automatic steps when updating
  - git pull origin master
  - docker-compose exec web bash
  - python manage.py migrate cyder
  - sudo supervisorctl restart all
  - Launch a the test suite (need one...)

Next steps:
  - Fix the general setting section
  - Create a graph of previous calibrations
  - Create search pages using Django filter (models and devices)
  - Create a page to create a project
  - Create a page to display models as a search
  - Separate the API from the views
  - Re-think the models to be including multiple models with transmission grid
  - Change ssh for celery workers
  - Create a script to update the system / or initialize.
