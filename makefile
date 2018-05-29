src/obsidian/grammar.py: src/grammar.ebnf
	tatsu src/grammar.ebnf -o src/obsidian/grammar.py

test: export PYTHONPATH=src
test: src/obsidian/grammar.py
	pytest

vtest: export PYTHONPATH=src
vtest: src/obsidian/grammar.py
	pytest -vv

test_prelude: export PYTHONPATH=src
test_prelude: src/obsidian/grammar.py
	pytest -vv tests/test_prelude.py

install: src/obsidian.vim
	cp -f src/obsidian.vim ~/.config/nvim/syntax

clean:
	rm -f src/obsidian/grammar.py
