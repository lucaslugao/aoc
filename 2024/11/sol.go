package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

var (
	countCache     = make(map[[2]int]int)
	transformCache = make(map[int][]int)
)

func count(stone int, blinks int) (res int) {
	key := [2]int{stone, blinks}
	if val, ok := countCache[key]; ok {
		return val
	}

	defer func() {
		countCache[key] = res
	}()

	if blinks == 0 {
		res = 1
		return
	}

	tvals := transform(stone)
	sum := 0
	for _, ns := range tvals {
		sum += count(ns, blinks-1)
	}
	res = sum
	return
}

func transform(stone int) (res []int) {
	if val, ok := transformCache[stone]; ok {
		return val
	}

	defer func() {
		transformCache[stone] = res
	}()

	if stone == 0 {
		res = []int{1}
		return
	}

	sstone := strconv.Itoa(stone)
	length := len(sstone)
	if length%2 == 0 {
		mid := length / 2
		leftPart := sstone[:mid]
		rightPart := sstone[mid:]

		leftVal, _ := strconv.Atoi(leftPart)
		rightVal, _ := strconv.Atoi(rightPart)
		res = []int{leftVal, rightVal}
		return
	}

	res = []int{stone * 2024}
	return
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	line := strings.TrimSpace(scanner.Text())
	parts := strings.Fields(line)

	var stones []int
	for _, p := range parts {
		val, _ := strconv.Atoi(p)
		stones = append(stones, val)
	}

	solution1 := 0
	solution2 := 0
	for _, s := range stones {
		solution1 += count(s, 25)
		solution2 += count(s, 75)
	}

	fmt.Println(solution1)
	fmt.Println(solution2)
}
