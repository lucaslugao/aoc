//go:build go_auto

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

	t_start := 0
	t_do := 4
	t_dont := 9
	t_mul := 13

	cTr := map[key]int{
		{t_start, 'd'}: 1,
		{1, 'o'}:       2,
		{2, '('}:       3,
		{3, ')'}:       t_do,
		{2, 'n'}:       5,
		{5, '\''}:      6,
		{6, 't'}:       7,
		{7, '('}:       8,
		{8, ')'}:       t_dont,
		{t_start, 'm'}: 10,
		{10, 'u'}:      11,
		{11, 'l'}:      12,
		{12, '('}:      t_mul,
	}

	t_mul1 := 14
	t_mul1c := 15
	t_mul2 := 16
	t_mul2c := 17

	for _, r := range "0123456789" {
		cTr[key{t_mul, r}] = t_mul1
		cTr[key{t_mul1, r}] = t_mul1
		cTr[key{t_mul1c, r}] = t_mul2
		cTr[key{t_mul2, r}] = t_mul2
	}

	cTr[key{t_mul1, ','}] = t_mul1c
	cTr[key{t_mul2, ')'}] = t_mul2c

	/* Visual representation of the automaton (* = digit)

	       ┌────┐   m   ┌───┐
	       │ 10 ◄───────┤ 0 ├t_start
	       └────┘       └─┬─┘
	          │u          │d
	       ┌──▼─┐       ┌─▼─┐
	       │ 11 │       │ 1 │
	       └──┬─┘       └─┬─┘
	          │l          │o
	       ┌──▼─┐       ┌─▼─┐ n   ┌───┐
	       │ 12 │       │ 2 ├─────► 5 │
	       └──┬─┘       └─┬─┘     └─┬─┘
	          │(          │(        │'
	       ┌──▼─┐       ┌─▼─┐     ┌─▼─┐
	       │ 13 ├t_mul  │ 3 │     │ 6 │
	       └──┬─┘       └─┬─┘     └─┬─┘
	          │*          │)        │t
	    ┌──┬──▼─┐       ┌─▼─┐     ┌─▼─┐
	   *└─►│ 14 ├t_mul1 │ 4 ├t_do │ 7 │
	       └──┬─┘       └───┘     └─┬─┘
	          │,                    │(
	       ┌──▼─┐                 ┌─▼─┐
	       │ 15 ├t_mul1c          │ 8 │
	       └──┬─┘                 └─┬─┘
	          │*                    │)
	    ┌──┬──▼─┐                 ┌─▼─┐
	   *└─►│ 16 ├t_mul2           │ 9 ├t_dont
	       └──┬─┘                 └───┘
	          │)
	       ┌──▼─┐
	       │ 17 ├t_mul2c
	       └────┘
	*/

	s, mul, cur, s_pos := 0, 0, 0, 0

	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		line := scanner.Text()
		for i, c := range line {
			if ns, ok := cTr[key{s, c}]; ok {
				s = ns
			} else if ns, ok := cTr[key{0, c}]; ok {
				s = ns
			} else {
				s = 0
			}

			switch s {
			case t_do:
				do = true
			case t_dont:
				do = false
			case t_mul:
				s_pos = i
			case t_mul1c:
				mul, _ = strconv.Atoi(line[s_pos+1 : i])
				s_pos = i
			case t_mul2c:
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
