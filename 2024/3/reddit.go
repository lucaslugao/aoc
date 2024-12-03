//go:build go_reddit

package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func readData(path string) string {
	file, err := os.Open(path)
	if err != nil {
		fmt.Printf("Error opening the file: %v", err)
	}
	defer file.Close()

	var corruptedMemory string

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		corruptedMemory += scanner.Text()
	}

	return corruptedMemory
}

func calcMul(mul string) int {
	cutPref, _ := strings.CutPrefix(mul, "mul(")
	cutSuff, _ := strings.CutSuffix(cutPref, ")")

	nums := strings.Split(cutSuff, ",")

	num1, _ := strconv.Atoi(nums[0])
	num2, _ := strconv.Atoi(nums[1])

	val := num1 * num2

	return val
}

func partOne(path string) int {
	corruptedMemory := readData(path)

	r, _ := regexp.Compile(`mul\(\d+,\d+\)`)
	matches := r.FindAllString(corruptedMemory, -1)

	var totalSum int
	for _, match := range matches {
		totalSum += calcMul(match)
	}

	return totalSum
}

func partTwo(path string) int {
	corruptedMemory := readData(path)

	r, _ := regexp.Compile(`mul\(\d+,\d+\)|don't\(\)|do\(\)`)
	matches := r.FindAllString(corruptedMemory, -1)

	enabled := true
	var totalSum int
	for _, match := range matches {
		if match == "don't()" {
			enabled = false
			continue
		}
		if match == "do()" {
			enabled = true
			continue
		}
		if enabled {
			totalSum += calcMul(match)
		}
	}

	return totalSum
}

func main() {
	fmt.Println(partOne(os.Args[1]))
	fmt.Println(partTwo(os.Args[1]))
}
