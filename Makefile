PYTHON = python

clean:
	@echo "Cleaning project..."
	rm -rf ./dist/
	rm -rf ./src/fail2ban_exporter.egg-info
	rm -rf ./build/
	rm -rf ./*.spec

flake8:
	@echo "Running flake8"
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

build: dependencies
	@echo "Building project"
	${PYTHON} -m  build

test: dependencies
	@echo "Running tests"
	${PYTHON} -m pipenv run ${PYTHON} -m unittest

package: dependencies
	@echo "Using pyinstaller to build executable"
	${PYTHON} -m pipenv run pyinstaller -n fail2ban_exporter --onefile ./src/fail2ban_exporter/__main__.py

dependencies: Pipfile.lock
	@echo "Install pipenv dependencies"
	${PYTHON} -m pipenv install -d
