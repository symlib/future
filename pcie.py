# coding=utf-8
# initial work on 2017.2.20
# this section includes list pd
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
Pass = "'result': 'p'"
Fail = "'result': 'f'"

def verifyPcie(c):
    FailFlag = False
    tolog("<b>Verify pcie </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify pcie </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPcielist(c):
    FailFlag = False
    tolog("<b>Verify pcie -a list </b>")

    if FailFlag:
        tolog('\n<font color="red">Fail: Verify pcie -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

def verifyPcieInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify pcie invalid option</b>")
    command = ['pcie -x', 'pcie -a list -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify pcie invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPcieInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify pcie invalid parameters</b>")
    command = ['pcie test', 'pcie -a test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify pcie invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyPcieMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify pcie missing parameters</b>")
    command = ['pcie -a ']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify pcie missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyPcie(c)
    verifyPcielist(c)
    verifyPcieInvalidOption(c)
    verifyPcieInvalidParameters(c)
    verifyPcieMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped