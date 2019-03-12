import json
import requests
import time
import sys
import os

from collections import OrderedDict
from urllib.parse import urlencode
from config import *
from StordGitBuildFio import *

VmId="1"
VmdkID="1"
TargetID="%s" %VmId
LunID="%s" %VmdkID

def truncate_disk(i, j):
    Name="iscsi-disk_%s_%s" %(i, j)
    Path="/var/hyc/%s" %(Name)
    cmd="sudo truncate --size=%sG %s" %(size_in_gb, Path)
    os.system(cmd);

    return Name, Path

def delete_vmdk(VmId, LunID, VmdkID):

    TargetID = VmId


    r = requests.post("%s://%s/tgt_svc/v1.0/lun_delete/?tid=%s&lid=%s" % (h, TgtUrl, TargetID, LunID), headers=headers, cert=cert, verify=False)
    print ("TGT: LUN %s deleted for VM: %s" %(LunID, TargetID))

    r = requests.post("%s://%s/stord_svc/v1.0/vmdk_delete/?vm-id=%s&vmdk-id=%s" % (h, StordUrl, VmId, VmdkID), headers=headers, cert=cert, verify=False)
    print ("STORD: VMDK %s deleted(vmdk_delete) for VM: %s" %(VmdkID, VmId))

def delete_vm(VmId):

    TargetID = VmId

    force_delete = 1
    r = requests.post("%s://%s/tgt_svc/v1.0/target_delete/?tid=%s&force=%s" % (h, TgtUrl, TargetID, force_delete), headers=headers, cert=cert, verify=False)
    print ("TGT: target %s deleted" %TargetID)

    r = requests.post("%s://%s/stord_svc/v1.0/vm_delete/?vm-id=%s" %(h, StordUrl, VmId))
    print ("STORD: target %s deleted" %VmId)


def deinit_components():

    data = { "service_type": "test_server", "service_instance" : 0, "etcd_ips" : "%s" %EtcdIps}
    r = requests.post("%s://%s/ha_svc/v1.0/component_stop" %(h, TgtUrl), data=json.dumps(data), headers=headers, cert=cert, verify=False)
    assert (r.status_code == 200)

    r = requests.post("%s://%s/ha_svc/v1.0/component_stop" %(h, StordUrl), data=json.dumps(data), headers=headers, cert=cert, verify=False)
    assert (r.status_code == 200)

def do_cleanup():
    os.system("lsblk")
    delete_vmdk(VmId, LunID, VmdkID)
    os.system("lsblk")
    #delete_vm(VmId)

    cmd = "sudo iscsiadm -m node --logout"
    os.system(cmd);

    cmd = "sudo iscsiadm -m node -o delete"
    os.system(cmd);

    time.sleep(5)
    os.system("lsblk")
 


#tgtd_args = '-f -e "http://127.0.0.1:2379" -s "tgt_svc" -v "v1.0" -p 9001 -D "127.0.0.1" -P 9876'.split()
#stord_args = '-etcd_ip="http://127.0.0.1:2379" -stord_version="v1.0" -svc_label="stord_svc" -ha_svc_port=9000 -v 1'.split()
tgtd_args = '-f -e http://127.0.0.1:2379 -s tgt_svc -v v1.0 -p 9001 -D 127.0.0.1 -P 9876'.split()
stord_args = '-etcd_ip=http://127.0.0.1:2379 -stord_version=v1.0 -svc_label=stord_svc -ha_svc_port=9000 -v 1'.split()
fio_args = '--name=random --ioengine=libaio --iodepth=32  --norandommap --group_reporting --gtod_reduce=1 --stonewall --rw=randrw --bs=16384 --direct=1 --size=102400 --numjobs=1 --rwmixread=1 --randrepeat=0 --filename=/dev/sdb --runtime=99999m --time_based=1 --size=10M'.split()

if __name__ == '__main__':
    cert = None
    if h == "https" :
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        h = "https"
        cert=('./cert/cert.pem', './cert/key.pem')

    print ("do_cleanup")
    do_cleanup()
    print ("deinit_components")
    deinit_components()


