from __future__ import division
import tool as t


def get(location, date_from, date_to):
    """Retrieve upmu data"""
    # Prepare input
    date_from = date_from.strftime("%Y-%m-%d_%H:%M:%S")
    if date_to:
        date_to = date_to.strftime("%Y-%m-%d_%H:%M:%S")
    else:
        date_to = "False"

    # Run ssh command
    timeout = 30
    cmd = "CyDER/web/docker_django/worker/upmu/get.py"
    arg = ['2016-12-15_12:00:00', '2016-12-15_12:02:00']
    output, status = t.run_ssh_command(cmd, timeout=timeout,
                                     server="cyder@bt-eplus.dhcp.lbl.gov", arg=arg)

    # Parse ssh output
    if output is not False:
        result = t.parse_ssh_list(output, status)
    else:
        raise Exception('SSH request to the server took more than ' +
                        str(timeout) + ' seconds')

    # Return a list of data from the upmu
    return result
