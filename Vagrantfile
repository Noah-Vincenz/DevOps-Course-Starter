Vagrant.configure("2") do |config|
	config.vm.box = "hashicorp/bionic64"
	config.vm.provision "shell", privileged: false, inline: <<-SHELL
		sudo apt-get update
		sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
		libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
		xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
		# To get rid of warning saying that pyenv is already installed
		# sudo rm -rf ~/.pyenv
		git clone https://github.com/pyenv/pyenv.git ~/.pyenv
		echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
		echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
		echo 'eval "$(pyenv init -)"' >> ~/.profile
		source ~/.profile
		pyenv install 3.8.5
		pyenv global 3.8.5
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
		# -n ("no-clobber") to avoid overwriting existing .env file
		cd /vagrant
		cp -n .env.template .env
	SHELL
  	config.vm.network "forwarded_port", guest: 5000, host: 5000
	config.trigger.after :up do |trigger|
		trigger.name = "Launching App"
		trigger.info = "Running the TODO app setup script"
		trigger.run_remote = {privileged: false, inline: "
			# install dependencies and launch
			cd /vagrant
			poetry install
			# instead of using 'poetry run flask run --host=0.0.0.0' we want to start it as a separate process and redirect console output to a file
			poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
		"}
	end
end
