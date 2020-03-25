import logging
import os
import random
import string
import sys

# Check if the below package is installed or not, if not installed install through pip
package = 'git'
try:
    __import__(package)
except ImportError:
    os.system('pip install gitpython')

import git

logger = logging.getLogger(__file__)


def check_imports_in_alphabetical_order(lines):
    try:
        empty_line_count = 0
        imports = []
        for line in lines:
            if line.startswith('import') or line.startswith('from'):
                if empty_line_count < 2:
                    imports.append(line)
                else:
                    empty_line_count += 1
                if empty_line_count > 2:
                    break

        line_count = 0
        imports_start_with_import = []
        for line in imports:
            if line.startswith('import'):
                line_count += 1
                imports_start_with_import.append(line)
            else:
                break
        imports_start_with_import = [line.split(' ')[-1].rstrip() for line in imports_start_with_import]
        # print(imports_start_with_import)
        if not sorted(imports_start_with_import) == imports_start_with_import:
            print(f'\n\t----\x1b[1;31m Please sort below imports in alphabetical order\x1b[0m ----\n\t', end='')
            print(imports_start_with_import)

        imports_start_with_from = []
        for line in imports[line_count:]:
            if line.startswith('from'):
                line_count += 1
                imports_start_with_from.append(line)
            else:
                break
        # print(imports_start_with_from)
        imports_start_with_from = [line.split(' ')[1] for line in imports_start_with_from]
    #     print(imports_start_with_from)
        if not sorted(imports_start_with_from) == imports_start_with_from:
            print(f'\n\t----\x1b[1;31m Please sort below imports in alphabetical order\x1b[0m ----\n\t', end='')
            print(imports_start_with_from)

        # print('sec_imports_start_with_import')
        sec_imports_start_with_import = []
        # print(imports[line_count+1:])
        for line in imports[line_count:]:
            if line.startswith('import'):
                line_count += 1
                sec_imports_start_with_import.append(line)
            else:
                break
        sec_imports_start_with_import = [line.split(' ')[-1].rstrip() for line in sec_imports_start_with_import]
        # print(sec_imports_start_with_import)
        if not sorted(sec_imports_start_with_import) == sec_imports_start_with_import:
            print(f'\n\t----\x1b[1;31m Please sort below imports in alphabetical order\x1b[0m ----\n\t', end='')
            print(sec_imports_start_with_import)

        sec_imports_start_with_from = []
        for line in imports[line_count:]:
            if line.startswith('from'):
                line_count += 1
                sec_imports_start_with_from.append(line)
            else:
                break
        # print(sec_imports_start_with_from)
        sec_imports_start_with_from = [line.split(' ')[1] for line in sec_imports_start_with_from]
        # print(sec_imports_start_with_from)
        if not sorted(sec_imports_start_with_from) == sec_imports_start_with_from:
            print(f'\n\t----\x1b[1;31m Please sort below imports in alphabetical order\x1b[0m ----\n\t', end='')
            print(sec_imports_start_with_from)
    except:
        pass


# Check word found in lines
def check_word(lines, word, is_print):
    # print(lines)
    is_word_found = False
    occurrences = []
    occurrence_lines = []
    line_count = 0
    try:
        for line in lines:
            if word in line:
                is_word_found = True
                occurrences.append(line_count)
                occurrence_lines.append(line)
            line_count += 1
        if not is_word_found and is_print:
            print(f'\t\x1b[1;31m{word} \x1b[0mis not found')
        return is_word_found, occurrences, occurrence_lines
    except:
        pass


def check_stage_attribute_lines_should_not_modified(tc_lines, word):
    repo = 'datacollector-tests'
    # It is a trigger for relative path and absolute path of test case file
    # If we use relative path to repo then it's value is True
    skip_changing_dir = False
    if repo not in file_name:
        skip_changing_dir = True
    previous_cwd = os.getcwd()
#     print(previous_cwd)
#     print('file_name ', file_name)
    try:
        if not skip_changing_dir:
            repo_full_path = file_name[:file_name.find(repo)+len(repo)]
            os.chdir(repo_full_path)
        repo = git.Repo()
        t = repo.head.commit.tree
        git_output = repo.git.diff(t).split('\n')
        # print(git_output)
        # print(check_word(git_output, word, False))
        is_word_found = check_word(git_output, word, False)[0]
        if is_word_found:
            # print(check_word(tc_lines, "@pytest.mark.parametrize('stage_attributes'", False))
            start_sa = check_word(tc_lines, word, False)[1][0]
            end_sa = start_sa
            while True:
                end_sa += 1
                if tc_lines[end_sa] == '@stub\n' or \
                        tc_lines[end_sa][:len('@pytest.mark')] == '@pytest.mark' or \
                        tc_lines[end_sa][:len('def test_')] == 'def test_' or \
                        tc_lines[end_sa][:len('@')] == '@':
                    break
            stage_attribute_lines = [line.rstrip() for line in tc_lines[start_sa: end_sa]]
            is_word_changed = False
            for sa_line in stage_attribute_lines:
                for git_line in git_output:
                    # print(git_line.find(sa_line))
                    if git_line.find(sa_line) != -1:
                        if git_line[0] == '-' or git_line[0] == '+':
                            # print(git_line)
                            print(f'\n\t\x1b[1;31m{word} \x1b[0mshould not be modified')
                            is_word_changed = True
                            break
                if is_word_changed:
                    break
        if not skip_changing_dir:
            os.chdir(previous_cwd)
    except:
        pass


def get_start_and_end_line_number_of_tc(lines, test_case):
    try:
        # print(test_case)
        # If test case name is not found in the file just return
        # print(check_word(lines, test_case, False))
        if len(check_word(lines, test_case, False)[1]) == 0:
            return 'skip_test_case'
        start_line_no = check_word(lines, test_case, False)[1][0]
        intial_start_line_no = start_line_no
        # print('test case starting line number: ', start_line_no, lines[start_line_no])
        # For starting line go up(decrement)
        # print(lines[start_line_no])
        while True:
            # print(lines[start_line_no])
            # Check '    pass\n' in above lines, if found it then stop going up
            if (lines[start_line_no] != '\n' and lines[start_line_no-1] == '\n' and lines[start_line_no-2] == '\n') or \
                    lines[start_line_no-2] == '    pass\n':
                break
            start_line_no -= 1
        end_line_no = intial_start_line_no+1
        # print('end_line_no ', end_line_no)
        # start_line_no += 1
        # print(lines[-5:])

        # Finding ending line
        while True:
            # print(lines[end_line_no])
            # print(lines[end_line_no])

            if end_line_no + 1 == len(lines):
                break
            # lines[end_line_no] = lines[end_line_no].rstrip()
            # print(lines[end_line_no])
            # if lines[end_line_no] != '\n' and lines[end_line_no + 1] == '\n':
            #     break
            if lines[end_line_no] == '@stub\n' or \
                    lines[end_line_no][:len('@pytest.mark')] == '@pytest.mark' or \
                    lines[end_line_no][:len('def test_')] == 'def test_' or \
                    lines[end_line_no][:len('@')] == '@':
                break
            end_line_no += 1

        # print(start_line_no, end_line_no)
        return start_line_no, end_line_no
    except:
        pass


def get_msg_in_warning_format(msg):
    return f'\x1b[1;31m{msg}\x1b[0m'


def two_blank_lines_before_and_after_fn(lines):
    try:
        tmp_file_dir = os.path.join('/tmp', 'a_' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))
        tmp_file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + '.py'
        tmp_file_path = os.path.join('/tmp', tmp_file_dir, tmp_file_name)
        #     print('temp file created in /tmp directory ', tmp_file_path)
        # Run shell command
        os.popen(f'mkdir {tmp_file_dir}').read().split('\n')
        # Write test case code to temp file
        with open(tmp_file_path, 'w') as file:
            file.write(''.join(lines))

        # Run pycodestyle command on temp file
        tmp_file_styles = os.popen(f'pycodestyle --max-line-length=120 {tmp_file_path}').read().split('\n')[:-1]

        # Removing W391 warning from tmp_file_styles
        new_tmp_file_styles = []
        for line in tmp_file_styles:
            tmp = line.split(':')
            # Skipping warning blank line at end of file
            if tmp[3][1:tmp[3].index(' ', 1)] == 'E302':
                new_tmp_file_styles.append(line)
        tmp_file_styles = new_tmp_file_styles

        if len(tmp_file_styles) > 0:
            print(f'\n\t-------------- Expected 2 blank lines, found 1 --------------')
        for line in tmp_file_styles:
            tmp = line.split(':')
            tmp[0] = file_name.split('/')[-1]
            # tmp[1] = str(int(tmp[1]) + start_line_no)
            tmp[1] = f'\x1b[0;32m{tmp[1]}\x1b[0m'
            tmp[3] = f"\x1b[1;31m{tmp[3][1:tmp[3].index(' ', 1)]}\x1b[0m{tmp[3][tmp[3].index(' ', 1):]}"
            print('\t' + ':'.join(tmp))
        os.system(f'rm -r {tmp_file_dir}')
    except:
        pass


def show_warnings_by_pycodestyle(tc_lines, start_line_no):
    try:
        tmp_file_dir = os.path.join('/tmp', 'a_'+''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))
        tmp_file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)) + '.py'
        tmp_file_path = os.path.join('/tmp', tmp_file_dir, tmp_file_name)
    #     print('temp file created in /tmp directory ', tmp_file_path)
        # Run shell command
        os.popen(f'mkdir {tmp_file_dir}').read().split('\n')
        # Write test case code to temp file
        with open(tmp_file_path, 'w') as file:
            file.write(''.join(tc_lines))

        # Run pycodestyle command on temp file
        tmp_file_styles = os.popen(f'pycodestyle --max-line-length=120 {tmp_file_path}').read().split('\n')[:-1]

        # Removing W391 warning from tmp_file_styles
        new_tmp_file_styles = []
        for line in tmp_file_styles:
            tmp = line.split(':')
            # Skipping warning blank line at end of file
            if tmp[3][1:tmp[3].index(' ', 1)] == 'W391':
                continue
            new_tmp_file_styles.append(line)
        tmp_file_styles = new_tmp_file_styles

        # print(tmp_file_styles)

        if len(tmp_file_styles) > 0:
            print(f'\n\t-------------- Code warnings by pycodestyle module --------------')
        for line in tmp_file_styles:
            tmp = line.split(':')
            tmp[0] = file_name.split('/')[-1]
            tmp[1] = str(int(tmp[1]) + start_line_no)
            tmp[1] = f'\x1b[0;32m{tmp[1]}\x1b[0m'
            tmp[3] = f"\x1b[1;31m{tmp[3][1:tmp[3].index(' ', 1)]}\x1b[0m{tmp[3][tmp[3].index(' ', 1):]}"
            print('\t'+':'.join(tmp))
        os.system(f'rm -r {tmp_file_dir}')
    except:
        pass


def get_words_should_not_be_present(tc_lines, word, start_line_no):
    try:
        # print(tc_lines)
        occurances = check_word(tc_lines, word, False)
    #     print(occurances)
        if len(occurances[1]) > 0:
            print(f'\t-------------- Remove \x1b[1;31m{word} \x1b[0mstatements in following lines --------------')
        for i in range(len(occurances[1])):
            print(f'\t\x1b[1;31m{occurances[1][i]+start_line_no+1}\x1b[0m {occurances[2][i]}', end='')
    #     print()
    except:
        pass


def find_all_indexes_of_ch(s, ch):
    try:
        return [i for i, ltr in enumerate(s) if ltr == ch]
    except:
        pass


def get_unnecessary_double_quote_lines(tc_lines, start_line_no):
    try:
        line_count = 1
        is_not_necessary_double_quotes_found = False
        for line in tc_lines:
            indexes_found = find_all_indexes_of_ch(line, '"')
            # print(indexes_found)
            # Considering this if condtion as doc string
            if '"""' in line:
                pass
            # If this (') charcter is found in the line then do not print the line to output.
            elif len(indexes_found) == 2:
                double_quotes_string = line[indexes_found[0]+1:indexes_found[1]]
                # print(tc_lines[line_count-1].split('"')[0])
                # print(find_all_indexes_of_ch(tc_lines[line_count-1].split('"')[0], "'"))

                # Skipping the line define with '(single quotes) and contains " in it, example
                # DATA = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache.gif HTTP/1.0" 200 232'
                if len(find_all_indexes_of_ch(tc_lines[line_count-1].split('"')[0], "'")) > 0:
                    continue
                # print(find_all_indexes_of_ch(tc_lines[line_count-1].split('"')[0], "'"))
            #     print(double_quotes_string)
                if "'" not in double_quotes_string:
                    if not is_not_necessary_double_quotes_found:
                        print(f'\n\t-------------- Remove double quotes in following lines --------------')
                    is_not_necessary_double_quotes_found = True
                    print(f'\t\x1b[1;31m{line_count + start_line_no}\x1b[0m ', line, end='')
        #             print(line_count + start_line_no, line, '')
            line_count += 1
    except:
        pass
# get_unnecessary_double_quote_lines(tc_lines)


def remove_commented_lines(tc_lines):
    new_tc_lines = []
    for line in tc_lines:
        if line.find('#') != -1:
            new_tc_lines.append(f"{line.split('#')[0]}#\n")
        else:
            new_tc_lines.append(line)
    return new_tc_lines


def all_fns_in_one_fn(lines, test_case):
    try:
        get_start_end_lines = get_start_and_end_line_number_of_tc(lines, test_case)
        # print('starting')
        if get_start_end_lines == 'skip_test_case':
            return
        start_line_no, end_line_no = get_start_end_lines
        # Extract test case lines from all the lines
        tc_lines = lines[start_line_no:end_line_no]
        # print(lines[start_line_no], lines[end_line_no])
        # print(tc_lines)

        # Skip the test cases which have @stub decorator
        stub_occurances = check_word(tc_lines, '@stub', False)
        pass_occurances = check_word(tc_lines, '    pass', False)
        pytest_mark_skip_occurances = check_word(tc_lines, '@pytest.mark.skip', False)
        # print(pass_occurances)
        # if test_case == 'test_quote_character':
        #     print(tc_lines)
        # print(tc_lines)
        # print(stub_occurances)
        if len(stub_occurances[1]) > 0 or len(pytest_mark_skip_occurances[1]) > 0:
            # print('\n--skipping ', test_case, ' test case')
            return

        # tc_lines = remove_commented_lines(tc_lines)

        print(f'\n ************** Following corrections are found in the test case \x1b[1;32m{test_case}\x1b[0m **************')

        # print(tc_lines)
        # Checking some literals should be present in the test case

        # print(tc_lines)
        check_word(tc_lines, 'DATA', True)
        check_word(tc_lines, 'EXPECTED_OUTPUT', True)
        check_word(tc_lines, 'keep_data', True)
        # print()
    #     check_word(lines, 'Pipeline Finisher Executor', True)

    #     print(tc_lines)
        get_words_should_not_be_present(tc_lines, 'print', start_line_no)

        # Some fields should not be changed   Ex: stage_attributes in test case
        check_stage_attribute_lines_should_not_modified(tc_lines, "@pytest.mark.parametrize('stage_attributes'")

        # show_warnings_by_pycodestyle(tc_lines, start_line_no)
        # get_unnecessary_double_quote_lines(tc_lines, start_line_no)
    except:
        pass


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1 or sys.argv[1] == '-h':
            print('Required arguments file_name, test_case_1, test_case_2, ....\n'
                  'If no test cases are passed, then script will check for all the test cases in the file.')
        file_name = sys.argv[1]
        test_cases = sys.argv[3:]
        # Read stage's test cases file
        with open(file_name, 'r') as f:
            lines = f.readlines()
        # print(lines)
        if len(test_cases) == 0:
            all_test_cases = check_word(lines, 'def test', False)[2]
            all_test_cases = ['test_'+tc.split('(')[0][len('def test')+1:] for tc in all_test_cases]
        #     print(all_test_cases)
    #         for test_case in all_test_cases:
    #             print(test_case)
            test_cases = all_test_cases
        for test_case in test_cases:
            all_fns_in_one_fn(lines, test_case)

        check_imports_in_alphabetical_order(lines)
        two_blank_lines_before_and_after_fn(lines)
        print()
    except:
        pass
