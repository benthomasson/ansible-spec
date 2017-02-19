PYTHON ?= python

.PHONY: develop
develop:
	$(PYTHON) setup.py develop

.PHONY: install
install:
	$(PYTHON) setup.py install

.PHONY: clean
clean:
	$(PYTHON) setup.py clean --all

.PHONY: test
test:
	./test/run.sh
