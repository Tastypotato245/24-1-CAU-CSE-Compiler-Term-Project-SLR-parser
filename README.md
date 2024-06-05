# 24-1-CAU-CSE-Compiler-Term-Project-SLR-parser
24-1-CAU-CSE-Compiler-Term-Project-SLR-parser

# How To Run?

```bash
python3 main.py {some_input_files.txt}
```

# How To Test?

in Linux or Mac... (or wsl in Window)

```bash
$ cd src/
$ ./random_test.sh
$ ./static_test.sh
```

## Example

```
➜  24-1-CAU-CSE-Compiler-Term-Project-SLR-parser git:(main) ✗ cd src
➜  src git:(main) ✗ ./random_test.sh
File generation complete.
Testing file rand_example/accept_01.test:
Testing file rand_example/accept_02.test:
Testing file rand_example/accept_03.test:

...

Testing file rand_example/reject_19.test:
Testing file rand_example/reject_20.test:

Final Summary:
Total Files Processed: 40
Total Cases: 39960
Total Passed Cases: 39991
Total Accepted Cases: 19991
Total Rejected Cases: 20000
Total Pass Percentage: 100.078%
Total Accept Percentage: 50.0275%
Total Reject Percentage: 50.0501%

Pass Percentage per File:
rand_example/accept_01.test: Passed: [#########################] 100%, Accepted: [#########################] 100%, Rejected: [##] 0%
rand_example/accept_02.test: Passed: [#########################] 100.1%, Accepted: [#########################] 100.1%, Rejected: [##] 0%
rand_example/accept_03.test: Passed: [#########################] 100.1%, Accepted: [#########################] 100.1%, Rejected: [##] 0%
rand_example/accept_04.test: Passed: [#########################] 100.1%, Accepted: [#########################] 100.1%, Rejected: [##] 0%

...

➜  src git:(main) ✗ ./static_test.sh
Testing file static_example/static_accept_case.txt:
File: static_example/static_accept_case.txt - Passed: 28 /       28 (100.00%)
Testing file static_example/static_reject_case.txt:
File: static_example/static_reject_case.txt - Passed: 50 /       50 (100.00%)
** PERFECT **

```

# DEV ENV

KYU : MacBook Air M1
HO  : Window11 wsl

```bash
$ python3 --version
Python 3.12.2
```

```bash
$ sw_vers
ProductName:		macOS
ProductVersion:		14.5
BuildVersion:		23F79v
```
