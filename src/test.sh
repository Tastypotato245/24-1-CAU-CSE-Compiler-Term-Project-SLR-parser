#!/bin/bash

# 1. example_maker.py 스크립트 실행
python3 example_maker.py 2>&1 | tee -a test.log

# 2. 로그 파일 초기화
log_file="test.log"
> "$log_file"

# 3. main.py 스크립트를 rand_example 디렉터리 내의 파일들에 대해 실행하고 결과를 percentage로 계산
total_files=0
total_cases=0
passed_cases=0
rejected_cases=0
other_cases=0

# 각 파일에 대한 결과를 저장할 배열
declare -a file_results

for file in rand_example/*; do
    file_total_cases=0
    file_passed_cases=0
    file_rejected_cases=0
    file_other_cases=0
    echo "Testing file $file:" | tee -a "$log_file"
    results=$(python3 main.py "$file" 2>&1)
    echo "$results" >> "$log_file"
    
    while IFS= read -r result; do
        file_total_cases=$((file_total_cases + 1))
        total_cases=$((total_cases + 1))
        if [[ $result == "ACCEPT" ]]; then
            file_passed_cases=$((file_passed_cases + 1))
            passed_cases=$((passed_cases + 1))
        elif [[ $result == "REJECT" ]]; then
            file_rejected_cases=$((file_rejected_cases + 1))
            rejected_cases=$((rejected_cases + 1))
        else
            file_other_cases=$((file_other_cases + 1))
            other_cases=$((other_cases + 1))
        fi
    done <<< "$results"

    if [ $file_total_cases -gt 0 ]; then
        file_passed_percentage=$(echo "scale=2; ($file_passed_cases / $file_total_cases) * 100" | bc)
        file_rejected_percentage=$(echo "scale=2; ($file_rejected_cases / $file_total_cases) * 100" | bc)
        file_other_percentage=$(echo "scale=2; ($file_other_cases / $file_total_cases) * 100" | bc)
        echo "File $file: Passed: $file_passed_cases / $file_total_cases ($file_passed_percentage%), Rejected: $file_rejected_cases / $file_total_cases ($file_rejected_percentage%), Other: $file_other_cases / $file_total_cases ($file_other_percentage%)" | tee -a "$log_file"
        file_results+=("$file $file_passed_percentage $file_rejected_percentage $file_other_percentage")
    else
        echo "File $file: No cases to test." | tee -a "$log_file"
        file_results+=("$file 0 0 0")
    fi
done

# 4. 전체 결과를 퍼센티지로 표시
if [ $total_cases -gt 0 ]; then
    passed_percentage=$(echo "scale=2; ($passed_cases / $total_cases) * 100" | bc)
    rejected_percentage=$(echo "scale=2; ($rejected_cases / $total_cases) * 100" | bc)
    other_percentage=$(echo "scale=2; ($other_cases / $total_cases) * 100" | bc)
    echo "Total Passed: $passed_cases / $total_cases ($passed_percentage%), Total Rejected: $rejected_cases / $total_cases ($rejected_percentage%), Total Other: $other_cases / $total_cases ($other_percentage%)" | tee -a "$log_file"
else
    echo "No cases to test." | tee -a "$log_file"
fi

# 5. 아스키 아트 그래프 출력
echo "" | tee -a "$log_file"
echo "Pass Percentage per File:" | tee -a "$log_file"
for result in "${file_results[@]}"; do
    file=$(echo $result | awk '{print $1}')
    passed_percentage=$(echo $result | awk '{print $2}')
    rejected_percentage=$(echo $result | awk '{print $3}')
    other_percentage=$(echo $result | awk '{print $4}')

    max_hashes=50
    passed_hashes=$(printf "%.0s#" $(seq 1 $(printf "%.0f" $(echo "($passed_percentage / 100) * $max_hashes" | bc))))
    rejected_hashes=$(printf "%.0s#" $(seq 1 $(printf "%.0f" $(echo "($rejected_percentage / 100) * $max_hashes" | bc))))
    other_hashes=$(printf "%.0s#" $(seq 1 $(printf "%.0f" $(echo "($other_percentage / 100) * $max_hashes" | bc))))

    # 색상 설정
    passed_color="\033[0;32m"  # 초록색
    rejected_color="\033[0;31m"  # 빨간색
    other_color="\033[0;33m"  # 노란색

    reset="\033[0m"

    echo -e "$file: Passed: [${passed_color}$passed_hashes${reset}] $passed_percentage%, Rejected: [${rejected_color}$rejected_hashes${reset}] $rejected_percentage%, Other: [${other_color}$other_hashes${reset}] $other_percentage%" | tee -a "$log_file"
done

