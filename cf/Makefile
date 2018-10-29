install:
	pip3 install . --user
	mkdir -p ~/.local/bin/
	cp cf.py ~/.local/bin/cf
	echo export PATH=\\044PATH:~/.local/bin >> ~/.bashrc
uninstall:
clean:
	rm -f ~/.local/bin/cf
	yes | pip3 uninstall cflib
