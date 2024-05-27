#!/bin/bash

# 디렉터리 및 파일 설정
accept_file="static_example/static_accept_case.txt"
reject_file="static_example/static_reject_case.txt"
log_file="static_test_log"
> "$log_file"

# 테스트 결과 초기화
total_cases=0
passed_cases=0
rejected_cases=0

# 예상치 못한 결과를 저장할 배열
declare -a unexpected_cases

# Function to run test cases
run_test_cases() {
    local file=$1
    local expected_result=$2

    echo "Testing file $file:" | tee -a "$log_file"
    results=$(python3 main.py "$file" 2>&1)
    echo "$results" >> "$log_file"
    
    line_num=1
    while IFS= read -r result; do
        line_content=$(sed "${line_num}q;d" "$file")
        if [[ $result == "HOGEUN_KYUSUNG_SLR_PARSER RESULT: ACCEPT" ]]; then
            if [[ $expected_result == "accept" ]]; then
                passed_cases=$((passed_cases + 1))
            else
                echo -e "\tERROR: Unexpected ACCEPT at $file:$line_num - $line_content" | tee -a "$log_file"
                unexpected_cases+=("\tERROR: Unexpected ACCEPT at $file:$line_num - $line_content")
            fi
        elif [[ $result == "HOGEUN_KYUSUNG_SLR_PARSER RESULT: REJECT" ]]; then
            if [[ $expected_result == "reject" ]]; then
                rejected_cases=$((rejected_cases + 1))
            else
                echo -e "\tERROR: Unexpected REJECT at $file:$line_num - $line_content" | tee -a "$log_file"
                unexpected_cases+=("\tERROR: Unexpected REJECT at $file:$line_num - $line_content")
            fi
        fi
        total_cases=$((total_cases + 1))
        line_num=$((line_num + 1))
    done <<< "$results"
}

# 테스트 실행
run_test_cases "$accept_file" "accept"
run_test_cases "$reject_file" "reject"

# 결과 출력
if [ $total_cases -gt 0 ]; then
    passed_percentage=$(echo "scale=2; ($passed_cases / $total_cases) * 100" | bc)
    rejected_percentage=$(echo "scale=2; ($rejected_cases / $total_cases) * 100" | bc)
    echo "Total Passed: $passed_cases / $total_cases ($passed_percentage%), Total Rejected: $rejected_cases / $total_cases ($rejected_percentage%)" | tee -a "$log_file"
else
    echo "No cases to test." | tee -a "$log_file"
fi

# 예상치 못한 결과 출력
if [ ${#unexpected_cases[@]} -eq 0 ]; then
    echo -e "\033[0;34m** PERFECT **\033[0m" | tee -a "$log_file"
else
    echo "Unexpected cases:" | tee -a "$log_file"
    for case in "${unexpected_cases[@]}"; do
        echo -e "$case" | tee -a "$log_file"
    done
fi

