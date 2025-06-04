#!
pytest  --alluredir=./allure-results

allure generate ./allure-results -o ./allure-report --clean


