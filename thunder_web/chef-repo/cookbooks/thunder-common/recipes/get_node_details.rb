# @author: Geo Varghese
# @create_date: 27-Apr-2015
# @modified by: Geo Varghese    
# @modified_date: 27-Apr-2015
# @linking to other page: 
# @description: The recipe to get network details of a node

showResultTag("TH_HEAD_RES")

# get network details
showResultSubTag("NIC_RES")
print node['network']
showResultSubTag("NIC_RES")

# get disk details
disk_details = executeCmdAndGetOutput("fdisk -l | awk '/Disk .* bytes/ {print $2 $5}'")
showResultSubTag("DISK_RES")
disk_list = disk_details.split(/\r?\n/)
print disk_list
showResultSubTag("DISK_RES")

# get cpu details
cpu_count = executeCmdAndGetOutput("nproc")
showResultSubTag("SYS_CPU")
print cpu_count
showResultSubTag("SYS_CPU")

# get ram details
ram_size = executeCmdAndGetOutput("free -m | awk '/Mem: / {print $2}'")
showResultSubTag("SYS_RAM")
print ram_size
showResultSubTag("SYS_RAM")

showResultTag("TH_FOOT_RES")