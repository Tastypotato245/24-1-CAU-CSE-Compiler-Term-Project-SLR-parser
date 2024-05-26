#!/bin/bash

# 1. example_maker.py 스크립트 실행
#python3 example_maker.py 2>&1 | tee -a test.log

# 2. 로그 파일 초기화
log_file="test.log"
> "$log_file"

# 3. main.py 스크립트를 rand_example 디렉터리 내의 파일들에 대해 실행하고 결과를 percentage로 계산
total_files=0
total_cases=0
passed_cases=0

# 각 파일에 대한 결과를 저장할 배열
declare -a file_results

for file in rand_example/*; do
    file_total_cases=0
    file_passed_cases=0
    echo "Testing file $file:" | tee -a "$log_file"
    results=$(python3 main.py "$file" 2>&1)
    echo "$results" >> "$log_file"
    while IFS= read -r result; do
        file_total_cases=$((file_total_cases + 1))
        total_cases=$((total_cases + 1))
        if [[ $result == "ACCEPT" ]]; then
            file_passed_cases=$((file_passed_cases + 1))
            passed_cases=$((passed_cases + 1))
        fi
    done <<< "$results"
    if [ $file_total_cases -gt 0 ]; then
        file_percentage=$(echo "scale=2; ($file_passed_cases / $file_total_cases) * 100" | bc)
        echo "File $file: Passed: $file_passed_cases / $file_total_cases ($file_percentage%)" | tee -a "$log_file"
        file_results+=("$file $file_percentage")
    else
        echo "File $file: No cases to test." | tee -a "$log_file"
        file_results+=("$file 0")
    fi
done

# 4. 전체 결과를 퍼센티지로 표시
if [ $total_cases -gt 0 ]; then
    percentage=$(echo "scale=2; ($passed_cases / $total_cases) * 100" | bc)
    echo "Total Passed: $passed_cases / $total_cases ($percentage%)" | tee -a "$log_file"
else
    echo "No cases to test." | tee -a "$log_file"
fi

# 5. 아스키 아트 그래프 출력
echo "" | tee -a "$log_file"
echo "Pass Percentage per File:" | tee -a "$log_file"
for result in "${file_results[@]}"; do
    file=$(echo $result | awk '{print $1}')
    percentage=$(echo $result | awk '{print $2}')
    graph=$(printf "%.0s#" $(seq 1 $(printf "%.0f" $percentage)))
    
    # 색상 설정
    if (( $(echo "$percentage < 50" | bc -l) )); then
        color="\033[0;31m"  # 빨간색
    elif (( $(echo "$percentage >= 50 && $percentage < 75" | bc -l) )); then
        color="\033[0;33m"  # 노란색
    else
        color="\033[0;32m"  # 초록색
    fi
    reset="\033[0m"

    echo -e "$file: [${color}$graph${reset}] $percentage%" | tee -a "$log_file"
done

