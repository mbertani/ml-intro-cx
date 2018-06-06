Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/xenial64"
  config.vm.network "forwarded_port", guest: 8888, host: 8888, host_ip: "127.0.0.1", id: 'ipyton-notebook-port'

  if Vagrant.has_plugin?("vagrant-vbguest") then
    config.vbguest.auto_update = false
  end
  config.vm.provider "virtualbox" do |vb|
   vb.memory = "2048"
   vb.cpus = 2
  end

  config.vm.hostname = "datavask-workshop"
  config.vm.provision "shell", inline: <<-SHELL
    # Update the system
	apt-get update
	apt-get -y upgrade
       apt-get install -y git
	# Download anaconda script
	wget -O anaconda.sh -nv https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh
	chmod +x anaconda.sh
	./anaconda.sh -b -p /usr/share/anaconda
	chown vagrant:vagrant /usr/share/anaconda
	rm anaconda.sh
	# Make conda available in the path
	echo export "PATH=/usr/share/anaconda/bin:\$PATH" >> /home/vagrant/.bashrc
	# update anaconda and install deep learning libraries
	/usr/share/anaconda/bin/conda update conda
	/usr/share/anaconda/bin/conda update anaconda
	/usr/share/anaconda/bin/conda install -c conda-forge tensorflow
	/usr/share/anaconda/bin/conda update ipython
	/usr/share/anaconda/bin/conda install -c conda-forge keras
	#interactive maps
	/usr/share/anaconda/bin/conda install -c conda-forge ipyleaflet
    	# widgets
	/usr/share/anaconda/bin/conda install -c conda-forge ipywidgets
	#lab
	/usr/share/anaconda/bin/conda install -c conda-forge jupyterlab

	#rebound
	/usr/share/anaconda/bin/pip install rebound
	/usr/share/anaconda/bin/conda install graphviz
       
        # LIME for explanations
        /usr/share/anaconda/bin/pip install lime

	# Add password to the jupyter notebook server
	mkdir /home/vagrant/.jupyter/ 
	chown vagrant:vagrant /home/vagrant/.jupyter/ 
	printf "c.NotebookApp.password = u'sha1:83aab2852741:71a56c4865ed39886d3742c4aac07fdd64489627'" > /home/vagrant/.jupyter/jupyter_notebook_config.py
	chown vagrant:vagrant /home/vagrant/.jupyter/jupyter_notebook_config.py
	# make startup script
	echo jupyter notebook --ip 0.0.0.0 --notebook-dir=/home/vagrant/ > /home/vagrant/run_jupyter.sh
	chmod +x /home/vagrant/run_jupyter.sh
	chown vagrant:vagrant /home/vagrant/run_jupyter.sh
	
        # log on to the box and run
	# $ ./run_jupyter.sh	
	# Go to you http://localhost:8888 and log on with the password "workshop"

        echo jupyter lab --ip 0.0.0.0 > /home/vagrant/run_lab.sh
        chmod +x /home/vagrant/run_lab.sh
        chown vagrant:vagrant /home/vagrant/run_lab.sh
        # Log into the box and run ./run_lab.sh then go to http://localhost:8888 and use "workshop" as password


	# The following are the particular dependencies for the workshop
	# clone the workshop repo
	git clone https://github.com/mbertani/ml-intro-cx.git
	chown -R vagrant:vagrant /home/vagrant/ml-intro-cx
   SHELL
  
end
