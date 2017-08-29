from __future__ import division
import docker_django.apps.cyder.models as m
import model_update as u
import models as m
import csv


def nodes():
    """
    """
    # Remove all the nodes
    nodes = m.Node.objects.all()
    for node in nodes:
        node.delete()

    all_models = m.Model.objects.all()
    for model in all_models:
        number_of_nodes = u.update_model_nodes(model.id)
        print("Updated " + str(model.filename) + ' with ' + str(number_of_nodes) + ' nodes.')

    return True


def devices():
    """
    """
    # Remove all the nodes
    devices = m.Devices.objects.all()
    for device in devices:
        device.delete()

    all_models = m.Model.objects.all()
    for model in all_models:
        number_of_devices = u.update_model_devices(model.id)
        print("Updated " + str(model.filename) + ' with ' + str(number_of_devices) + ' nodes.')

    return True


def feeders(filename='/usr/src/app/docker_django/static/init_DB.csv'):
    """
    Initialize the database from a csv file.
    (remove previous instances)
    To do:
        - do not remove previous instances and just update from csv files
        - add more details about each models
    """
    # Counter
    model_added = 0

    # Remove existing model from the database
    all_model = m.Model.objects.all()
    for instance in all_model:
        instance.delete()

    # Read csv file
    with open(filename, 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        # Each row define a distribution grid model
        for row in spamreader:
            new_entry = {
                'filename': row['filename'],
                'lat': row['lat'],
                'lon': row['lon'],
                'breaker_name': row['breaker_name'],
                'city': row['city'],
                'area': row['area'],
                'region': row['region'],
                'zip_code': row['zip_code'],
                'version': row['version'],
                'upmu_location': row['upmu_location'],
            }

            new_model = m.Model(**new_entry)
            new_model.save()
            model_added += 1

    print("You have added " + str(model_added) + " distribution models")
    return True
