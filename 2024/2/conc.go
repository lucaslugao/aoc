//go:build go_conc

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
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

	for i, field := range fields {
		num, err := strconv.Atoi(field)
		if err == nil {
			nums[i] = num
		}
	}
	return nums
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <filename> <nWorkers:5>")
		os.Exit(1)
	}

	filename := os.Args[1]

	nWorkers := 5
	if len(os.Args) > 2 {
		n, err := strconv.Atoi(os.Args[2])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Invalid number of workers: %v\n", os.Args[2])
		}
		nWorkers = n
	}

	var solution1 int64
	var solution2 int64
	var wg sync.WaitGroup

	for i := 0; i < nWorkers; i++ {
		wg.Add(1)
		go func(workerID int) {
			defer wg.Done()

			var pSolution1 int64
			var pSolution2 int64

			file, err := os.Open(filename)
			if err != nil {
				fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
				return
			}
			defer file.Close()
			currentLine := -1
			scanner := bufio.NewScanner(file)

			for scanner.Scan() {
				currentLine++
				if currentLine%nWorkers != workerID {
					continue
				}
				nums := parseLine(scanner.Text())
				if nums == nil {
					continue
				}
				v := valid(nums, -1)
				if v {
					pSolution1 += 1
				}
				if v || validIgnoringOne(nums) {
					pSolution2 += 1
				}
			}
			atomic.AddInt64(&solution1, pSolution1)
			atomic.AddInt64(&solution2, pSolution2)

			if err := scanner.Err(); err != nil {
				fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
			}
		}(i)
	}

	wg.Wait()

	fmt.Println(solution1)
	fmt.Println(solution2)
}
