src/obsidian/grammar.py: src/grammar.ebnf
	tatsu src/grammar.ebnf -o src/obsidian/grammar.py

test: export PYTHONPATH=src
test: src/obsidian/grammar.py
	pytest

vtest: export PYTHONPATH=src
vtest: src/obsidian/grammar.py
	pytest -vv

clean:
	rm -f src/obsidian/grammar.py
