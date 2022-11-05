coverage run --omit=./encoder/tests/* --source=encoder.lib --branch --module encoder.tests._run_all
coverage html
./htmlcov/index.html