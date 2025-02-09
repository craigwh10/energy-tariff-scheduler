.PHONY: build
build:
	rm -rf dist
	rm -rf energy_tariff_scheduler.egg-info
	.venv/bin/python -m build -v
	pip uninstall energy_tariff_scheduler
	pip install dist/energy_tariff_scheduler-1.0.0-py3-none-any.whl

.PHONY: test-go
test-go:
	python ./_test_go_script.py

.PHONY: test-agile
test-agile:
	python ./_test_agile_script.py

.PHONY: deploy
deploy:
	twine upload dist/*