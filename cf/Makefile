MATCHLEN := $(shell egrep "export PATH=\\\$$PATH\\:~/.local/bin" ~/.bashrc | wc -c)

install:
	pip3 install . --user
	mkdir -p ~/.local/bin/
	cp cf.py ~/.local/bin/cf
	@if [ $(MATCHLEN) -eq 0 ]; then \
		echo 'export PATH=$$PATH:~/.local/bin' >> ~/.bashrc;\
	fi
clean:
	rm -f ~/.local/bin/cf
	yes | pip3 uninstall cflib
test:
	python3 -m unittest discover

install2:
	pip install . --user
	mkdir -p ~/.local/bin/
	cp cf.py ~/.local/bin/cf
	@if [ $(MATCHLEN) -eq 0 ]; then \
		echo 'export PATH=$$PATH:~/.local/bin' >> ~/.bashrc;\
	fi
clean2:
	rm -f ~/.local/bin/cf
	yes | pip uninstall cflib
test2:
	python -m unittest discover
