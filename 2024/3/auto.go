//go:build go_automtok

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func main() {
	var solution1, solution2 int
	do := true

	type key struct {
		state int
		char  rune
	}

	t_do := 6
	t_dont := 10
	t_mul := 13
	t_mul1 := 14
	t_mul1f := 15
	t_mul2 := 16
	t_mul2f := 17

	cTr := map[key]int{
		{0, 'd'}:  1,
		{1, 'o'}:  3,
		{3, '('}:  4,
		{4, ')'}:  t_do,
		{3, 'n'}:  5,
		{5, '\''}: 7,
		{7, 't'}:  8,
		{8, '('}:  9,
		{9, ')'}:  t_dont,
		{0, 'm'}:  2,
		{2, 'u'}:  11,
		{11, 'l'}: 12,
		{12, '('}: t_mul,
	}

	for _, r := range "0123456789" {
		cTr[key{t_mul, r}] = t_mul1
		cTr[key{t_mul1, r}] = t_mul1
		cTr[key{t_mul1f, r}] = t_mul2
		cTr[key{t_mul2, r}] = t_mul2
	}

	cTr[key{t_mul1, ','}] = t_mul1f
	cTr[key{t_mul2, ')'}] = t_mul2f

	state, mul, cur, s_pos := 0, 0, 0, 0

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		for i, c := range line {
			if newState, ok := cTr[key{state, c}]; ok {
				state = newState
			} else if newState, ok := cTr[key{0, c}]; ok {
				state = newState
			} else {
				state = 0
			}

			switch state {
			case t_do:
				do = true
			case t_dont:
				do = false
			case t_mul:
				s_pos = i
			case t_mul1f:
				mul, _ = strconv.Atoi(line[s_pos+1 : i])
				s_pos = i
			case t_mul2f:
				cur, _ = strconv.Atoi(line[s_pos+1 : i])
				solution1 += mul * cur
				if do {
					solution2 += mul * cur
				}
			}
		}
	}

	fmt.Println(solution1)
	fmt.Println(solution2)
}
