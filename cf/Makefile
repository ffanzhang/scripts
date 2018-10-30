install:
	pip3 install . --user
	mkdir -p ~/.local/bin/
	cp cf.py ~/.local/bin/cf
	echo 'export PATH=$$PATH:~/.local/bin' >> ~/.bashrc
uninstall:
clean:
	rm -f ~/.local/bin/cf
	yes | pip3 uninstall cflib
test:
	python3 -m unittest discover

