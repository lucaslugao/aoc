package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func isSolvable(target int, nums []int, concat bool) (result bool) {
	if len(nums) == 1 {
		return target == nums[0]
	}

	lnum := nums[len(nums)-1]
	nnums := nums[:len(nums)-1]

	if target >= lnum && isSolvable(target-lnum, nnums, concat) {
		return true
	}

	if target%lnum == 0 && isSolvable(target/lnum, nnums, concat) {
		return true
	}

	if concat {
		factor := int(math.Pow(10, float64(len(strconv.Itoa(lnum)))))
		if target >= factor && target%factor == lnum {
			if isSolvable(target/factor, nnums, concat) {
				return true
			}
		}
	}
	return false
}

func main() {
	solution1 := 0
	solution2 := 0

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Split(line, ":")
		if len(parts) != 2 {
			continue
		}

		target, err := strconv.Atoi(strings.TrimSpace(parts[0]))
		if err != nil {
			fmt.Fprintf(os.Stderr, "Invalid target: %v\n", err)
			continue
		}

		numsStr := strings.Fields(strings.TrimSpace(parts[1]))
		nums := make([]int, len(numsStr))
		for i, numStr := range numsStr {
			nums[i], err = strconv.Atoi(numStr)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Invalid number in list: %v\n", err)
				continue
			}
		}

		if isSolvable(target, nums, false) {
			solution1 += target
		}
		if isSolvable(target, nums, true) {
			solution2 += target
		}
	}

	fmt.Println(solution1)
	fmt.Println(solution2)
}
