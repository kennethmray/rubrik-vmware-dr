##########
#
# my OCD caused me to put this 1992 author note.
# author: Ken Ray
#
##########

import rubrik_cdm
import urllib3
import getpass
import datetime
import os

# using this to disable the self-signed cert warning...it bugs me. 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# this is the name of the colon-delimeted (that doesn't sound right) text file containing vm-name:esx-host
vm_file         = 'vm.txt'

# this is to use the Windows cls system command to clear the screen. Now, if this were linux it would be 'clear'.
os.system('cls')

# these are the prompts to gather the Rubrik Cluster Name and the appropriate credentals.
rubrik_cluster  = input('\n\n Please enter DR Rubrik Cluster Name or IP: ')
rubrik_username = input(' Please enter your Username: ')
rubrik_password = getpass.getpass(' Please enter your Password: ')

# this actually makes the connection to the Rubik Cluster, imagine that. 
rubrik = rubrik_cdm.Connect(node_ip=rubrik_cluster, username=rubrik_username, password=rubrik_password)

# yep, this tells you what it's about to do, asks if your cool with it, and then rips apart your text file to know which vm to Live Mount where.
# oh, and then it Live Mounts it there.
def start_replica_vm_livemount(filehandle):
    print ('\n Initiating VM Live Mount(s) at DR on ['+datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")+']')
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
        print ('\n Completed on: ['+datetime.datetime.now().strftime("%a, %d %B %Y %H:%M:%S")+']')
    else:
        print ('\n Cancelled.\n')
        exit()

# which snapshot, or point in time copy of your precious vm do we want to run over there, in DR? Guess what? It's gonna be the latest PIT copy.
def get_snapshot_id(vm_id):
    snaps = rubrik.get('v1', '/vmware/vm/'+vm_id+'/snapshot')
    for snap in snaps['data']:
        return snap['id']

# we have to know the Rubrik vmId of the vm that we want to Live Mount, duh!?
def get_vm_id(vm_name):
    vms = rubrik.get('v1', '/vmware/vm')    
    for vm in vms['data']:
        if vm['name'] == vm_name:
            return vm['id']

# this gets called to figure out the Rubrik hostId for the esx host where we want the vm to run.
def get_host_id(host_name):
    hosts = rubrik.get('v1', '/vmware/host')    
    for host in hosts['data']:
        if host['name'] == host_name:
            return host['id']


# this right here is where it really gets going...no, seriously. So, here we call the function to actually start the Live Mounts.
def main():
    start_replica_vm_livemount(filehandle = open(vm_file, 'r'))
    

# this is where we start the program, spoiler alert, it's gonna call the function above called... main.

main()