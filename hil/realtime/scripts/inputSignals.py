
# This script is used to extract the names of
# the OPAL-RT FMU inputs
# The name of the file which contains
# the name of the FMU is OPALRTFMU.log
# This file is generated when running the python
# script which invokes the OPAL-RT FMU
# so it can read input and output names

import os
fil=open('OPALRTFMU.log', 'r')
content=fil.read()
fil.close()
content=content.split(',')
#print(content)
inputs=[]
for idx, val in enumerate(content):
    if val==" (OP_CONTROL_SIGNAL":
        inputs.append(content[idx+2])

if os.path.exists("inputNames.txt"):
    os.remove("inputNames.txt")
fil=open("inputNames.txt", 'w')
fil.write(str(inputs))
fil.close()
