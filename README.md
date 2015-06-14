# Thunder Engine

This repository represents the AQORN Thunder Engine, its dependencies and installation instructions.

Thunder is a GUI based software tool for deployment and management of OpenStack based clusters. It is developed using Django and allows end to end deployment of OpenStack clusters through a simple, coherent and comprehensive Graphical User Interface.

Documentation of Thunder can be found at http://docs.aqorn.com/thunder/

A live demo of Thunder is available at http://www.thunder-demo.com

Thunder Community will be avauilable soon with a bunch of extra features that leverage this engine. Visit http://www.aqorn.com/products

Prerequisites for Thunder setup
===============================

You only need internet access for fetching the Thunder files from this repo. No internet access is required on the actual machine on which it is installed.

Only the main Thunder Node need to be present in the network during initial installation. Additional nodes can be added later on which will be auto detected.

Please go through the planning guide(http://docs.aqorn.com/thunder/) section of Thunder docs to allocate and setup resources in advance.

Installing Thunder
======================

Thunder installation happens in few simple steps. Initial phase consist of installing a base image and fetching Thunder. Next step is to run basic installer from backend which is followed by verification and configuration via browser.

Steps for installation
----------------------

1.Fetch and install base OS on main Thunder node:

    # wget http://releases.ubuntu.com/trusty/ubuntu-14.04.2-desktop-amd64.iso
    
    
Burn and install this base ISO on the machine designated as main Thunder hardware node. Restart the computer when prompted after removing cdrom.

2.To fetch the latest source and base OS images, run these:

    # git clone https://github.com/AQORN/thunder-community
    # wget http://old-releases.ubuntu.com/releases/12.04.2/ubuntu-12.04.2-server-amd64.iso
    # cp ubuntu-12.04.2-server-amd64.iso thunder-community/system/

3.Run initial installer script from console to setup base packages and env.

    # chmod +x thunder-community/system/thunder_build.sh
    # thunder-community/system/thunder_build.sh
    

  This would take a while as it has to install various packages and copy files to appropriate locations.

4.Complete env verification and package setup

    # http:localhost:9000/

  Open Firefox and go to http://localhost:9000/ for completing package setup.
 
 
5.Configure Thunder: This step allows you to setup login credentials, configure network etc.

  Note: Once above step has been completed successfully, you will be automatically redirected to this section

    # http:localhost:9000/
    
 Once this step has been completed, you can access Thunder from http://localhost:9000/

You can ssh to Thunder node using username which you provided during installation of base os.
