black --exclude "usr|.venv" .
find . -type f -name "*.py" | xargs pylint 
bandit --verbose *.py && bandit --verbose tests/*.py -c bandit.yml