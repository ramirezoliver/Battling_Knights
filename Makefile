.PHONY: test
test:
	coverage run --source=app -m pytest tests/ut

.PHONY: run_moves
run_moves:
	python app/main.py
