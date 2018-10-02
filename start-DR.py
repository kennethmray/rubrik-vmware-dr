import rubrik_cdm
import urllib3
import getpass
import datetime
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

vm_file         = 'vm.txt'

os.system('cls')

rubrik_cluster  = input('\n\n Please enter DR Rubrik Cluster Name or IP: ')
rubrik_username = input(' Please enter your Username: ')
rubrik_password = getpass.getpass(' Please enter your Password: ')

try:
    rubrik = rubrik_cdm.Connect(node_ip=rubrik_cluster, username=rubrik_username, password=rubrik_password)
except:
    print ('\n Error Connecting to DR Rubrik Cluster!\n')
    exit()


def start_replica_vm_livemount(filehandle):
    print ('\n Initiating DR VM Live Mount(s) ['+datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")+']')
    keep_going = input(' Continue \'Y\' or \'N\': ')
    if keep_going in ['y', 'Y']:
        for line in filehandle:
            l = line.rstrip().split(':')
            print ('\n Live Mounting: '+l[0]+' on ESX Host: '+l[1], end='')
            snap_id = get_snapshot_id(get_vm_id(l[0]))
            host_id = get_host_id(l[1])
            host = {}
            host['hostId'] = host_id
            lm_results = rubrik.post('v1', '/vmware/vm/snapshot/'+snap_id+'/mount', host)
            print (' ...', lm_results['status']+'!')
        print ('\n Completed on: '+datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S"))
    else:
        print ('\n Cancelled.\n')
        exit()


def get_snapshot_id(vm_id):
    snaps = rubrik.get('v1', '/vmware/vm/'+vm_id+'/snapshot')
    for snap in snaps['data']:
        return snap['id']


def get_vm_id(vm_name):
    vms = rubrik.get('v1', '/vmware/vm')    
    for vm in vms['data']:
        if vm['name'] == vm_name:
            return vm['id']


def get_host_id(host_name):
    hosts = rubrik.get('v1', '/vmware/host')    
    for host in hosts['data']:
        if host['name'] == host_name:
            return host['id']


def main():
    start_replica_vm_livemount(filehandle = open(vm_file, 'r'))
    

# start program

main()