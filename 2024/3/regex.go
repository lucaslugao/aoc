//go:build go_regex

package main

import (
	"bufio"
	"fmt"
	"os"
	"regexp"
	"strconv"
)

var (
	mulPattern       = regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	betweenDoAndDont = regexp.MustCompile(`do\(\)(?s:(.*?))don't\(\)`)
)

func doMul(data []string) int {
	total := 0
	for _, d := range data {
		for _, match := range mulPattern.FindAllStringSubmatch(d, -1) {
			x, _ := strconv.Atoi(match[1])
			y, _ := strconv.Atoi(match[2])
			total += x * y
		}
	}
	return total
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var data string
	data += "do()"
	for scanner.Scan() {
		data += scanner.Text()
	}
	data += "don't()"

	solution1 := doMul([]string{data})
	var matches []string
	for _, match := range betweenDoAndDont.FindAllStringSubmatch(data, -1) {
		matches = append(matches, match[1])
	}

	solution2 := doMul(matches)

	fmt.Println(solution1)
	fmt.Println(solution2)
}
