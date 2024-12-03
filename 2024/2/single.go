//go:build go_single

package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"runtime/pprof"
	"strconv"
	"strings"
)

func valid(row []int, skip int) bool {
	n := len(row)

	prev := -1
	pdiff := 0

	for i := 0; i < n; i++ {
		if i == skip {
			continue
		}

		if prev == -1 {
			prev = i
			continue
		}

		diff := row[i] - row[prev]

		if diff == 0 || diff < -3 || diff > 3 {
			return false
		}

		if pdiff == 0 {
			pdiff = diff
		} else if pdiff*diff <= 0 {
			return false
		}

		prev = i
	}
	return true
}

func validIgnoringOne(row []int) bool {
	for i := 0; i < len(row); i++ {
		if valid(row, i) {
			return true
		}
	}
	return false
}

func parseLine(line string) []int {
	fields := strings.Fields(line)
	nums := make([]int, len(fields))
	count := 0

	for _, field := range fields {
		num, err := strconv.Atoi(field)
		if err == nil { // Only process valid numbers
			nums[count] = num
			count++
		}
	}
	if count == 0 {
		return nil
	}
	return nums[:count]
}

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

func main() {
	flag.Parse()
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		pprof.StartCPUProfile(f)
		defer pprof.StopCPUProfile()
	}

	var solution1 int64
	var solution2 int64

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		nums := parseLine(line)
		if nums == nil {
			continue
		}
		v := valid(nums, -1)
		if v {
			solution1 += 1
		}
		if v || validIgnoringOne(nums) {
			solution2 += 1
		}
	}

	fmt.Println(solution1)
	fmt.Println(solution2)
}
