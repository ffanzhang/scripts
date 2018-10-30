install:
	pip3 install . --user
	pip3 install requests --user
	mkdir -p ~/.local/bin/
	cp cf.py ~/.local/bin/cf
	echo export PATH=\\044PATH:~/.local/bin >> ~/.bashrc
uninstall:
clean:
	rm -f ~/.local/bin/cf
	yes | pip3 uninstall cflib
test_install:
	pip3 install requests_mock
test:
	python3 -m unittest discover

