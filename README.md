# test_case_check
First please add absolute path of check.py file in ~/.bashrc, like below

    alias check='f(){ python /home/shravank/test_case_check/check.py $1 $*; unset -f f;};f'



Then, we can run the check command in both the ways(absolute and relative paths)

    check stage/configuration/test_mqtt_subscriber_origin.py
    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py

It's mandetory to give which test case file(stage) in the first argument of check command and afterwards specify test case names with space seperated like below.

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py test_directory_origin_configuration_file_name_pattern

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py test_directory_origin_configuration_file_name_pattern test_directory_origin_configuration_file_name_pattern_mode


If we don't specify any test case name after the file name, then script will check for all the test cases in the file.

    check /home/shravank/project/gerrit/datacollector-tests/stage/configuration/test_directory_origin.py
