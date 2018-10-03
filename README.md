# rubrik-vmware-dr

This will 'Live Mount' user specified Rubrik replicated VMs at a remote location. (oh, and the script is in Python)

A colon-delimited text file lists the VMs and the Host you would like the VMs to run. 

Example of colon delimited text file, named vm.txt in the same folder/directory as the script:

	vm-name1:vm-host1
	vm-name2:vm-host2
	vm-name3:vm-host2
	vm-name4:vm-host3

Running the script on Windows: (just make sure python.exe is in the path and the vm.txt file exists with the script.

	python start-DR.py
