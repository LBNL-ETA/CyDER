from celery import shared_task
import datetime

@shared_task
def test():
    # Get the current time
    now = datetime.datetime.now()

    # Write the time in a file
    with open('/usr/src/app/QQQQQQQQQQQQ.txt', 'a') as the_file:
        the_file.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        the_file.write("\n")

    # Return a success
    return True
