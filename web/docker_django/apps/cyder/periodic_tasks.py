from celery import shared_task
import datetime

@shared_task
def test(arg):
    # Get the current time
    now = datetime.datetime.now()

    # Write the time in a file
    with open('../celery_beat_test.txt', 'a') as the_file:
        the_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        the_file.write("\n")

    # Return a success
    return True
