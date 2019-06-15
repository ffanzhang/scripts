MATCHLEN := $(shell egrep "export PATH=\\\$$PATH\\:~/.local/bin" ~/.bashrc | wc -c)

install:
	chmod +x *.sh
	mkdir -p ~/.local/bin/
	cp gg.sh ~/.local/bin/gg
	cp pp.sh ~/.local/bin/pp
	cp p3.sh ~/.local/bin/p3
	cp grab.sh ~/.local/bin/grab
	cp create_test_file_if_missing.sh ~/.local/bin/
	@if [ $(MATCHLEN) -eq 0 ]; then \
		@echo 'export PATH=$$PATH:~/.local/bin' >> ~/.bashrc; \
	fi \

	@if ! [ -d ~/.local/bin/src ]; then \
		git clone https://github.com/ffanzhang/lib ~/.local/bin/src/; \
	else \
		cd ~/.local/bin/src; \
		git stash branch master; \
		git pull origin master; \
	fi \

clean:
	rm ~/.local/bin/gg
	rm ~/.local/bin/pp
	rm ~/.local/bin/p3
	rm ~/.local/bin/create_test_file_if_missing.sh
	rm -rf ~/.local/bin/src
