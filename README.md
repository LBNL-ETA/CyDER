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
  - python manage.py shell
  - import docker_django.apps.cyder.manual_functions as f
  - f.database_initialization()

None automatic steps when updating
  - git pull origin master
  - docker-compose exec web bash
  - python manage.py migrate cyder
  - sudo supervisorctl restart all
  - Launch a the test suite (need one...)

Current task: Finish calibration process with new upmu data
  - add breaker number and id type in arg
Next steps:
  - Add a setting page with a menu of actions
  - Change markers for dots?
  - Create a graph of previous calibrations
  - Create a REST API
  - Create a Upmu page
  - Create search pages using Django filter (models and devices)
  - Change ssh for celery workers
  - Create a script to update the system / or initialize.
