//go:build go_conc

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
)

// Grid represents a 2D grid of characters.
type Grid struct {
	data []string
	w    int
	h    int
}

// NewGrid initializes a new Grid with the given data.
func NewGrid(data []string) *Grid {
	if len(data) == 0 {
		return &Grid{data: data, w: 0, h: 0}
	}
	w := len(data[0])
	h := len(data)
	return &Grid{data: data, w: w, h: h}
}

// At returns the character at position (x, y) or "." if out of bounds.
func (g *Grid) At(x, y int) string {
	if x < 0 || x >= g.w || y < 0 || y >= g.h {
		return "."
	}
	return string(g.data[y][x])
}

// Coord represents a coordinate in the grid.
type Coord struct {
	x int
	y int
}

func countXmas(grid *Grid, nWorkers int) int {
	neigh := [8][2]int{
		{0, 1},
		{0, -1},
		{1, 0},
		{-1, 0},
		{1, 1},
		{-1, -1},
		{1, -1},
		{-1, 1},
	}

	hasXmasAt := func(x, y, dx, dy int) bool {
		target := "XMAS"
		for i, c := range target {
			if grid.At(x+i*dx, y+i*dy) != string(c) {
				return false
			}
		}
		return true
	}

	var wg sync.WaitGroup
	countChan := make(chan int, nWorkers)

	for worker := 0; worker < nWorkers; worker++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			localCount := 0
			for y := 0; y < grid.h; y++ {
				for x := 0; x < grid.w; x++ {
					if (x+y*grid.w)%nWorkers != i {
						continue
					}
					for _, direction := range neigh {
						dx, dy := direction[0], direction[1]
						if hasXmasAt(x, y, dx, dy) {
							localCount++
						}
					}
				}
			}
			countChan <- localCount
		}(worker)
	}

	wg.Wait()
	close(countChan)

	totalCount := 0
	for c := range countChan {
		totalCount += c
	}
	return totalCount
}

func countXMAs(grid *Grid, nWorkers int) int {
	coordsFormMas := func(coords [][2]int) bool {
		s := ""
		for _, coord := range coords {
			s += grid.At(coord[0], coord[1])
		}
		return s == "MAS" || s == "SAM"
	}

	hasCrossAt := func(x, y int) bool {
		diagonals := [2][3][2]int{
			{
				{x - 1, y - 1},
				{x, y},
				{x + 1, y + 1},
			},
			{
				{x - 1, y + 1},
				{x, y},
				{x + 1, y - 1},
			},
		}
		for _, diagonal := range diagonals {
			coords := [][2]int{
				{diagonal[0][0], diagonal[0][1]},
				{diagonal[1][0], diagonal[1][1]},
				{diagonal[2][0], diagonal[2][1]},
			}
			if !coordsFormMas(coords) {
				return false
			}
		}
		return true
	}

	var wg sync.WaitGroup
	countChan := make(chan int, nWorkers)

	for worker := 0; worker < nWorkers; worker++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			localCount := 0
			for y := 0; y < grid.h; y++ {
				for x := 0; x < grid.w; x++ {
					if (x+y*grid.w)%nWorkers != i {
						continue
					}
					if hasCrossAt(x, y) {
						localCount++
					}
				}
			}
			countChan <- localCount
		}(worker)
	}

	wg.Wait()
	close(countChan)

	totalCount := 0
	for c := range countChan {
		totalCount += c
	}
	return totalCount
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <filename> <nWorkers:10>")
		os.Exit(1)
	}
	filename := os.Args[1]
	file, err := os.Open(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	data := []string{}
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line != "" {
			data = append(data, line)
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "Error reading input:", err)
		os.Exit(1)
	}

	grid := NewGrid(data)
	nWorkers := 10
	if len(os.Args) > 2 {
		n, err := strconv.Atoi(os.Args[2])
		if err != nil {
			fmt.Fprintf(os.Stderr, "Invalid number of workers: %v\n", os.Args[2])
		}
		nWorkers = n
	}

	xmasCount := countXmas(grid, nWorkers)
	xmasAsCount := countXMAs(grid, nWorkers)

	fmt.Println(xmasCount)
	fmt.Println(xmasAsCount)
}
