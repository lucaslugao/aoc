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
	mulDoDontPattern = regexp.MustCompile(`mul\((\d+),(\d+)\)|do\(\)|don't\(\)`)
)

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var data string
	do := true
	solution1 := 0
	solution2 := 0
	for scanner.Scan() {
		data = scanner.Text()

		for _, match := range mulDoDontPattern.FindAllStringSubmatch(data, -1) {
			if match[0] == "do()" {
				do = true
			} else if match[0] == "don't()" {
				do = false
			} else {
				x, _ := strconv.Atoi(match[1])
				y, _ := strconv.Atoi(match[2])
				v := x * y
				solution1 += v
				if do {
					solution2 += v
				}
			}

		}
	}

	fmt.Println(solution1)
	fmt.Println(solution2)
}
