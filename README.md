# test_case_check
First clone this repository and please add absolute path of check.py file in ~/.bashrc, like below

    alias check='f(){ python /home/shravank/test_case_check/check.py $1 $*; unset -f f;};f'

Install git module through pip

    pip install gitpython

Then, we can run the check command in both the ways(relative and absolute paths)

    check stage/configuration/test_mqtt_subscriber_origin.py

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py

It's mandetory to give which test case file(stage) in the first argument of check command and afterwards specify test case names with space seperated like below.

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py test_case_1

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py test_case_1 test_case_2


If we don't specify any test case name after the file name, then script will check for all the test cases in the file.

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py
