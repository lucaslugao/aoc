//go:build go_naive

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
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

// countXmas counts the number of times "XMAS" appears in the grid in any of the 8 directions.
func countXmas(grid *Grid) int {
	neigh := [8][2]int{
		{0, 1},   // Down
		{0, -1},  // Up
		{1, 0},   // Right
		{-1, 0},  // Left
		{1, 1},   // Down-Right
		{-1, -1}, // Up-Left
		{1, -1},  // Up-Right
		{-1, 1},  // Down-Left
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

	count := 0
	for y := 0; y < grid.h; y++ {
		for x := 0; x < grid.w; x++ {
			for _, direction := range neigh {
				dx, dy := direction[0], direction[1]
				if hasXmasAt(x, y, dx, dy) {
					count++
				}
			}
		}
	}
	return count
}

// countXMAs counts the number of times a cross pattern with "MAS" or "SAM" appears in both diagonals.
func countXMAs(grid *Grid) int {
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

	count := 0
	for y := 0; y < grid.h; y++ {
		for x := 0; x < grid.w; x++ {
			if hasCrossAt(x, y) {
				count++
			}
		}
	}
	return count
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
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
	fmt.Println(countXmas(grid))
	fmt.Println(countXMAs(grid))
}
