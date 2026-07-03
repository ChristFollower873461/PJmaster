PYTHON ?= python3

.PHONY: qa test scan disc label

qa: test scan disc

test:
	$(PYTHON) -m unittest discover -s tests

scan:
	$(PYTHON) tools/scan_public_safety.py .

label:
	$(PYTHON) tools/create_cd_label.py

disc: label
	$(PYTHON) tools/build_disc_package.py
