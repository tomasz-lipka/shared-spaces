# shared-spaces
Enhanced version of the application to share thoughts between family members and friends

+-------------------------------------------------+

ACTIVATING VIRTUAL ENV

. .venv/bin/activate

+-------------------------------------------------+

TESTING

execute from ../project

all classes:

python -m unittest

single class

python -m unittest test.test_assignment_controller

+-------------------------------------------------+

TEST WITH COVERAGE

coverage run -m unittest

coverage html

+--------------------------------------------------+
LYNTING
pylint assignment_service.py


## Test coverage at 99%
Coverage report
![coverage-report](./readme/image/coverage-report.jpg)