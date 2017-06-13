# coding=utf-8
# initial sample work on 2016.12.23
# this section includes verify proper cmd/parameters/options and
# some other boundary or misspelled parameters/options
from send_cmd import *
from to_log import *
from ssh_connect import ssh_conn
from pool import getavailpd
from pool import bvtsparedelete
from pool import poolcleanup
from pool import poolcreateandlist
from pool import sparedrvcreate

import random
Pass = "'result': 'p'"
Fail = "'result': 'f'"
def findPdId(c):
    result = SendCmd(c, 'phydrv')
    pdID = []
    row = result.split('\r\n')
    if 'Error (' not in result:
        for r in range(4, (len(row) -1)):
            if row[r].split()[-1] != 'Unconfigured':
                pdID.append(row[r].split()[0])
    return pdID
def verifyBBM(c):
    FailFlag = False
    for i in findPdId(c):
        tolog('\n<b> Verify bbm -p ' + i)
        result = SendCmd(c, 'bbm -p ' + i)
        if 'Error (' in result:
            FailFlag = True
            tolog('<font color="red">Fail: bbm -p ' + i + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMList(c):
    FailFlag = False
    for i in findPdId(c):
        tolog('\n<b> Verify bbm -a list -p ' + i)
        result = SendCmd(c, 'bbm -a list -p ' + i)
        if 'Error (' in result:
            FailFlag = True
            tolog('<font color="red">Fail: bbm -a list -p ' + i + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm -a list </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMClear(c):
    FailFlag = False
    tolog("<b>Verify bbm -a clear -p pd ID (configured SATA physical drive)</b>")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST":
            tolog('\n<font color="red">Fail: there is no SAST type PD</font>')
            break
        if row.split()[2] == "SAST" and row.split()[-1] != "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    if len(pdid) != 0:
        for m in pdid:
            result = SendCmd(c, "bbm -a clear " + m)
            if "Error (" in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: Verify bbm -a clear ' + m + '</font>')
    if FailFlag:
        tolog('\n<font color="red">Verify bbm -a clear -p pd ID (configured SATA physical drive)</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMHelp(c):
    FailFlag = False
    tolog("<b>Verify bbm -h</b>")
    result = SendCmd(c, "bbm -h")
    if "Usage" not in result or "Summary" not in result or "bbm" not in result:
        FailFlag = True
        tolog('\n<font color="red">Fail: bbm -h </font>')
    if FailFlag:
        tolog('\n<font color="red">Verify bbm -h </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMClearFailedTest(c):
    FailFlag = False
    tolog("<b>Verify bbm -a clear -p pd id (unconfigured SATA physical drive)</b>")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST":
            tolog('\n<font color="red"> Fail: there is no SAST type PD </font>')
            break
        if row.split()[2] == "SAST" and row.split()[-1] != "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    if len(pdid) != 0:
        for m in pdid:
            result = SendCmd(c, "bbm -a clear " + m)
            if "Error" in result:
                FailFlag = True
                tolog('\n<font color="red">Fail: Verify bbm -a clear ' + m + '</font>')

    tolog("<b> Verify bbm -a clear -p pd id(configured not SATA physical drive)</b>")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST" and row.split()[-1] == "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a clear -p " + Rpdid)
    if "Error" not in result:
        FailFlag =True
        tolog('\n<font color="red">Fail: bbm -a clear -p ' + Rpdid + '</font>')

    tolog("<b>Verify bbm -a clear -p pd id(Unconfigured not SATA physical drive)</b>")
    result = SendCmd(c, "phydrv")
    num = 4
    pdid = []
    while result.split("\r\n")[num] != 'administrator@cli> ':
        row = result.split("\r\n")[num]
        if row.split()[2] != "SAST" and row.split()[-1] == "Unconfigured":
            pdid.append(row.split()[0])
        num = num + 1
    Rpdid = random.choice(pdid)
    result = SendCmd(c, "bbm -a clear -p " + Rpdid)
    if "Error" not in result:
        FailFlag =True
        tolog('\n<font color="red">Fail: bbm -a clear -p ' + Rpdid + '</font>')

    tolog("<b> Verify bbm -a clear -p pd's ID </b>")
    result = SendCmd(c, "bbm -a clear -p 1")
    if "Error" not in result:
        FailFlag = True
        tolog('\n<font color="red"> Fail: bbm -a clear -p pd ID </font>')

    if FailFlag:
        tolog('\n<font color="red">Verify bbm -a clear failed test</font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMSpecifyInexistentId(c):
    FailFlag = False
    tolog("<b>Verify bbm specify inexistent CtrlId</b>")
    command = ['bbm -p 256', 'bbm -a list -p 256', 'bbm -a clear -p 256']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "nvalid physical drive id" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm specify inexistent CtrlId </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMInvalidOption(c):
    FailFlag = False
    tolog("<b>Verify bbm invalid option</b>")
    command = ['bbm -x', 'bbm -a list -x', 'bbm -a clear -x']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid option" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm invalid option </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMInvalidParameters(c):
    FailFlag = False
    tolog("<b>Verify ctrl invalid parameters</b>")
    command = ['bbm test', 'bbm -a test', 'bbm -a clear -p test']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Invalid setting parameters" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm invalid parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)
def verifyBBMMissingParameters(c):
    FailFlag = False
    tolog("<b>Verify bbm missing parameters</b>")
    command = ['bbm -p', 'bbm -a list -p', 'bbm -a clear -p']
    for com in command:
        tolog('<b> Verify ' + com + '</b>')
        result = SendCmd(c, com)
        if "Error (" not in result or "Missing parameter" not in result:
            FailFlag = True
            tolog('\n<font color="red">Fail: ' + com + ' </font>')
    if FailFlag:
        tolog('\n<font color="red">Fail: Verify bbm missing parameters </font>')
        tolog(Fail)
    else:
        tolog('\n<font color="green">Pass</font>')
        tolog(Pass)

if __name__ == "__main__":
    start = time.clock()
    c, ssh = ssh_conn()
    verifyBBM(c)
    verifyBBMList(c)
    verifyBBMClear(c)
    verifyBBMHelp(c)
    verifyBBMClearFailedTest(c)
    verifyBBMSpecifyInexistentId(c)
    verifyBBMInvalidOption(c)
    verifyBBMInvalidParameters(c)
    verifyBBMMissingParameters(c)
    ssh.close()
    elasped = time.clock() - start
    print "Elasped %s" % elasped