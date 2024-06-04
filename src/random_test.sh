#!/bin/bash

# 1. example_maker.py 스크립트 실행
python3 example_maker.py 2>&1 | tee -a test.log

# 2. 로그 파일 초기화
log_file="random_test.log"
> "$log_file"

# 임시 결과 파일 초기화
result_dir=$(mktemp -d)
trap "rm -rf $result_dir" EXIT

process_file() {
    local file=$1
    local result_file="$result_dir/$(basename "$file").result"
    local file_total_cases=0
    local file_passed_cases=0
    local file_accepted_cases=0
    local file_rejected_cases=0

    # 파일의 총 라인 수 계산
    file_total_cases=$(wc -l < "$file")

    echo "Testing file $file:" | tee -a "$log_file"
    results=$(python3 main.py "$file" 2>&1)
    echo "$results" >> "$log_file"
    
    line_num=0
    while IFS= read -r result; do
        line_num=$((line_num + 1))
        if [[ $result == "HOGEUN_KYUSUNG_SLR_PARSER RESULT: ACCEPT" ]]; then
            file_accepted_cases=$((file_accepted_cases + 1))
            if [[ $file == *"accept_"* ]]; then
                file_passed_cases=$((file_passed_cases + 1))
            else
                echo -e "\tERROR: Unexpected ACCEPT at $file:$line_num" | tee -a "$log_file"
            fi
        elif [[ $result == "HOGEUN_KYUSUNG_SLR_PARSER RESULT: REJECT" ]]; then
            file_rejected_cases=$((file_rejected_cases + 1))
            if [[ $file == *"reject_"* ]]; then
                file_passed_cases=$((file_passed_cases + 1))
            else
                echo -e "\tERROR: Unexpected REJECT at $file:$line_num" | tee -a "$log_file"
            fi
        fi
    done <<< "$results"

    file_passed_percentage=$(awk "BEGIN {print ($file_passed_cases / $file_total_cases) * 100}")
    file_accepted_percentage=$(awk "BEGIN {print ($file_accepted_cases / $file_total_cases) * 100}")
    file_rejected_percentage=$(awk "BEGIN {print ($file_rejected_cases / $file_total_cases) * 100}")

    echo "$file $file_total_cases $file_passed_cases $file_accepted_cases $file_rejected_cases $file_passed_percentage $file_accepted_percentage $file_rejected_percentage" > "$result_file"
}

export -f process_file
export log_file
export result_dir

# 병렬로 파일 처리
find rand_example/* -type f | xargs -n 1 -P 4 -I {} bash -c 'process_file "$@"' _ {}

# 최종 결과 집계
total_files=0
total_cases=0
passed_cases=0
accepted_cases=0
rejected_cases=0
declare -a file_results

for result_file in "$result_dir"/*.result; do
    read -r file file_total_cases file_passed_cases file_accepted_cases file_rejected_cases file_passed_percentage file_accepted_percentage file_rejected_percentage < "$result_file"
    file_results+=("$file $file_passed_percentage $file_accepted_percentage $file_rejected_percentage")
    total_files=$((total_files + 1))
    total_cases=$((total_cases + file_total_cases))
    passed_cases=$((passed_cases + file_passed_cases))
    accepted_cases=$((accepted_cases + file_accepted_cases))
    rejected_cases=$((rejected_cases + file_rejected_cases))
done

# 전체 결과를 퍼센티지로 표시
if [ $total_cases -gt 0 ]; then
    passed_percentage=$(awk "BEGIN {print ($passed_cases / $total_cases) * 100}")
    accepted_percentage=$(awk "BEGIN {print ($accepted_cases / $total_cases) * 100}")
    rejected_percentage=$(awk "BEGIN {print ($rejected_cases / $total_cases) * 100}")
else
    passed_percentage=0
    accepted_percentage=0
    rejected_percentage=0
fi

# 최종 요약 결과 출력
echo "" | tee -a "$log_file"
echo "Final Summary:" | tee -a "$log_file"
echo "Total Files Processed: $total_files" | tee -a "$log_file"
echo "Total Cases: $total_cases" | tee -a "$log_file"
echo "Total Passed Cases: $passed_cases" | tee -a "$log_file"
echo "Total Accepted Cases: $accepted_cases" | tee -a "$log_file"
echo "Total Rejected Cases: $rejected_cases" | tee -a "$log_file"
echo "Total Pass Percentage: $passed_percentage%" | tee -a "$log_file"
echo "Total Accept Percentage: $accepted_percentage%" | tee -a "$log_file"
echo "Total Reject Percentage: $rejected_percentage%" | tee -a "$log_file"

# 아스키 아트 그래프 출력
echo "" | tee -a "$log_file"
echo "Pass Percentage per File:" | tee -a "$log_file"

max_hashes=25  # 최대 해시 갯수를 줄여서 라인이 너무 길어지지 않도록 설정

for result in "${file_results[@]}"; do
    file=$(echo $result | awk '{print $1}')
    passed_percentage=$(echo $result | awk '{print $2}')
    accepted_percentage=$(echo $result | awk '{print $3}')
    rejected_percentage=$(echo $result | awk '{print $4}')

    passed_hashes_count=$(awk "BEGIN {print int(($passed_percentage / 100) * $max_hashes)}")
    accepted_hashes_count=$(awk "BEGIN {print int(($accepted_percentage / 100) * $max_hashes)}")
    rejected_hashes_count=$(awk "BEGIN {print int(($rejected_percentage / 100) * $max_hashes)}")

    passed_hashes=$(printf "%.0s#" $(seq 1 $passed_hashes_count))
    accepted_hashes=$(printf "%.0s#" $(seq 1 $accepted_hashes_count))
    rejected_hashes=$(printf "%.0s#" $(seq 1 $rejected_hashes_count))

    # 색상 설정
    passed_color="\033[0;32m"  # 초록색
    accepted_color="\033[0;34m"  # 파란색
    rejected_color="\033[0;33m"  # 주황색

    reset="\033[0m"

    echo -e "$file: Passed: [${passed_color}$passed_hashes${reset}] $passed_percentage%, Accepted: [${accepted_color}$accepted_hashes${reset}] $accepted_percentage%, Rejected: [${rejected_color}$rejected_hashes${reset}] $rejected_percentage%" | tee -a "$log_file"
done

if [ $passed_cases -eq $total_cases ]; then
    echo -e "\033[0;34m** PERFECT **\033[0m" | tee -a "$log_file"
fi

