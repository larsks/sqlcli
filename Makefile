PYTHON=python
DESTDIR=/
prefix=/usr

all: build/lib/sqlcli/__init__.py

build/lib/sqlcli/__init__.py: $(wildcard sqlcli/*.py)
	$(PYTHON) setup.py build

install: all
	$(PYTHON) setup.py install --root=$(DESTDIR) --prefix=$(prefix) \
		--skip-build -O1

