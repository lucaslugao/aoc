package main

import (
	"bufio"
	"container/heap"
	"fmt"
	"math"
	"os"
)

type Point struct {
	x, y int
}

type Direction struct {
	dx, dy int
}

type State struct {
	pos Point
	dir Direction
}

var TURN_CW = map[Direction]Direction{
	{1, 0}:  {0, 1},  // E -> S
	{0, 1}:  {-1, 0}, // S -> W
	{-1, 0}: {0, -1}, // W -> N
	{0, -1}: {1, 0},  // N -> E
}

var TURN_CCW = map[Direction]Direction{
	{1, 0}:  {0, -1}, // E -> N
	{0, 1}:  {1, 0},  // S -> E
	{-1, 0}: {0, 1},  // W -> S
	{0, -1}: {-1, 0}, // N -> W
}

func (r *State) forward() State {
	return State{pos: Point{r.pos.x + r.dir.dx, r.pos.y + r.dir.dy}, dir: r.dir}
}
func (r *State) back() State {
	return State{pos: Point{r.pos.x - r.dir.dx, r.pos.y - r.dir.dy}, dir: r.dir}
}
func (r *State) turn() [2]State {
	return [2]State{
		{pos: r.pos, dir: TURN_CW[r.dir]},
		{pos: r.pos, dir: TURN_CCW[r.dir]},
	}
}

type Grid struct {
	data  map[Point]bool
	w, h  int
	start Point
	end   Point

	cost     map[State]int
	min_cost int
}

func NewGrid(lines []string) *Grid {
	g := &Grid{}
	g.h = len(lines)
	g.data = make(map[Point]bool)
	if g.h > 0 {
		g.w = len(lines[0])
	}

	// Fill data map
	for y, row := range lines {
		for x, ch := range row {
			if ch == '#' {
				continue
			}
			p := Point{x, y}
			g.data[p] = true
			switch ch {
			case 'S':
				g.start = p
			case 'E':
				g.end = p
			}
		}
	}

	g.cost = make(map[State]int)
	g.min_cost = math.MaxInt32

	return g
}

func (g *Grid) at(p Point) bool {
	val, ok := g.data[p]
	return val && ok
}

// Item for priority queue
type Item struct {
	cost  int
	state State
	index int
}

// PriorityQueue implements heap.Interface
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].cost < pq[j].cost
}
func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}
func (pq *PriorityQueue) Push(x interface{}) {
	item := x.(*Item)
	item.index = len(*pq)
	*pq = append(*pq, item)
}
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	*pq = old[0 : n-1]
	return item
}

func (g *Grid) solve() bool {
	startDir := Direction{1, 0} // Facing east first
	startState := State{pos: g.start, dir: startDir}
	g.cost[startState] = 0

	pq := &PriorityQueue{}
	heap.Init(pq)
	heap.Push(pq, &Item{cost: 0, state: State{pos: g.start, dir: startDir}})

	visited := make(map[State]bool)

	for pq.Len() > 0 {
		item := heap.Pop(pq).(*Item)
		cost, state := item.cost, item.state

		if state.pos == g.end {
			g.min_cost = cost
			return true
		}

		if visited[state] {
			continue
		}
		visited[state] = true

		// Prune if we have already found a better path
		if x, ok := g.cost[state]; ok && x < cost {
			continue
		}

		// Turn
		for _, nextState := range state.turn() {
			if x, ok := g.cost[nextState]; !ok || cost+1000 < x {
				g.cost[nextState] = cost + 1000
				heap.Push(pq, &Item{cost: cost + 1000, state: nextState})
			}
		}

		// Move
		nextState := state.forward()
		if g.at(nextState.pos) {
			if x, ok := g.cost[nextState]; !ok || cost+1 < x {
				g.cost[nextState] = cost + 1
				heap.Push(pq, &Item{cost: cost + 1, state: nextState})
			}
		}
	}

	return false
}

func (g *Grid) count_best() int {
	queue := []State{}
	visited := make(map[State]bool)
	for _, d := range TURN_CCW {
		st := State{pos: g.end, dir: d}
		if x, ok := g.cost[st]; ok && x == g.min_cost {
			queue = append(queue, st)
			visited[st] = true
		}
	}

	cells := make(map[Point]bool)
	for len(queue) > 0 {
		state := queue[0]
		queue = queue[1:]
		dist := g.cost[state]
		cells[state.pos] = true

		// Backtracking turns:
		for _, prevState := range state.turn() {
			if !visited[prevState] {
				if x, ok := g.cost[prevState]; ok && x+1000 == dist {
					visited[prevState] = true
					queue = append(queue, prevState)
				}
			}
		}

		// Backtracking moves:
		prevState := state.back()
		if g.at(prevState.pos) {
			if !visited[prevState] {
				if x, ok := g.cost[prevState]; ok && x+1 == dist {
					visited[prevState] = true
					queue = append(queue, prevState)
				}
			}
		}
	}

	return len(cells)
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	var data []string
	for scanner.Scan() {
		line := scanner.Text()
		data = append(data, line)
	}

	grid := NewGrid(data)
	if grid.solve() {
		fmt.Println(grid.min_cost)
		fmt.Println(grid.count_best())
	}
}
