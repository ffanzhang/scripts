MATCHLEN := $(shell egrep "export PATH=\\\$$PATH\\:~/.local/bin" ~/.bashrc | wc -c)

install:
	chmod +x *.sh
	mkdir -p ~/.local/bin/
	cp gg.sh ~/.local/bin/gg
	cp pp.sh ~/.local/bin/pp
	cp p3.sh ~/.local/bin/p3
	cp create_test_file_if_missing.sh ~/.local/bin/
	@if [ $(MATCHLEN) -eq 0 ]; then \
		echo 'export PATH=$$PATH:~/.local/bin' >> ~/.bashrc;\
	fi

clean:
	rm -f ~/.loacl/bin/gg
	rm -f ~/.loacl/bin/pp
	rm -f ~/.loacl/bin/p3
	rm -f ~/.loacl/bin/create_test_file_if_missing
