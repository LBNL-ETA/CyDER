<<<<<<< HEAD
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
=======
# Cyber Physical Co-simulation Platform for Distributed Energy Resources (CyDER)


## Overview

CyDER is a modular and scalable tool for power system planning and operation that will work seamlessly with existing interconnection planning tools in the utilities and be interoperable with future utility software, data streams, and controls. CyDER will maintain and enhance the efficiency and reliability of the power system in a cost-effective and safe manner, being built on three pillars: quasi-static time series (QSTS) co-simulation and optimization, real-time data acquisition, and hardware-in-the-loop (HIL) application.

## Download

Files can be downloaded individually, or as a whole repository.

See the _Clone_ button on the top right for instructions and for programs that use a graphical user interfaces.

To download, edit and add files from a command line, install first a `git` program.

To download all files, run

    git clone https://YOURLOGIN@bitbucket.org/berkeleylab/cyder.git

The edit a file, such as `README.md`, first edit the file, then enter

    git commit -m "Revised README file" README.md
    git push

To add new files, enter something like

    git add filename.xyz
    git commit -m "Added the file xxxx" filename.xyz
    git push
    
To use the git command on `Windows`

1. download and install a `git` client such as [github desktop](https://desktop.github.com/)[^install] 

2. open the Git Shell

3. From the Git Shell command prompt, 

    create a folder which should contain the files on the CyDER repository by typing

        mkdir cyder-repo

4. change to the created folder by typing

        cd cyder-repo

From the Github Shell command prompt, you can execute any `git` command.

To download, edit, and add new files see the commands listed in the section above.

[^install]: In the installation process, you might be asked to log into your repository, just skip this section.
>>>>>>> p2
