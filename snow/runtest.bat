#! 收集并执行所有测试，并生成 Allure 报告数据
pytest --reruns 1 --reruns-delay 1 --alluredir=./allure-results
allure generate ./allure-results -o ./allure-report --clean
