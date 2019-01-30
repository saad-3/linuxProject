# Catalog Item Project
## project Description

in this project we will create a web app that have technology brands , and each brand have one or more than one product under it and store it in database called "techbrands.db" , and you can add a product to specific brand if and only if you are signed in with google account , and also you can edit or delete your own product that you have created .

to create this app we will use  python code in the python file "project.py" and we will use sqlalchemy module to do the sql querys .
and also we will use flask framework .


## Requirements
  1. vagrant    https://www.vagrantup.com/downloads.html
  2. virtualbox   https://www.virtualbox.org/wiki/Downloads
  3. udacity virtual machine    https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip


## Installation
### install the virtual machine
after you download vagrant and virtualbox and udacity virtual machine follow
these steps :
1. run your terminal, inside the vagrant subdirectory,
 run the command "vagrant up". This will cause Vagrant to download
 the Linux operating system and install it. This may take quite a
  while (many minutes) depending on how fast your Internet connection is.
2. When "vagrant up" is finished running, you can run "vagrant ssh"
to log in to your newly installed Linux VM!

* in the local machine , move the folder "catalogProject" to "vagrant" subdirectory to sync it with the VM.



### create the database
to create the database follow these steps :
1. run the virtual machine by following the steps above .
2. cd to "/vagrant/catalogProject" .
3. in the terminal write the command "python database_setup.py" to create an empty database with the Required tables .
4. in the terminal run the command "python demoDB.py" to add demo user , brand and products to the database.


## Start Up
after you finished the Installation guide above, you are ready to start the application .

to start the app follow these steps :
1. run the virtual machine and cd to "/vagrant/catalogProject"
2. in the terminal run the command "python project.py"
3. open your browser and go to "http://localhost:5000"


if you see the main page that contain brands and recently added product , then you are done . 
