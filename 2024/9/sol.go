package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
)

type Disk struct {
	blocks     []int
	fileBlocks map[int][]int
}

func NewDisk(data []int) *Disk {
	sum := 0
	for _, v := range data {
		sum += v
	}

	d := &Disk{
		blocks:     make([]int, sum),
		fileBlocks: make(map[int][]int),
	}
	for i := range d.blocks {
		d.blocks[i] = -1
	}

	pos := 0
	for i := 0; i < len(data); i++ {
		if i%2 == 0 {
			d.insertFile(i/2, pos, data[i])
			pos += data[i]
		} else {
			pos += data[i]
		}
	}

	return d
}

func (d *Disk) insertFile(idx, pos, size int) {
	for i := 0; i < size; i++ {
		d.blocks[pos+i] = idx
		d.fileBlocks[idx] = append(d.fileBlocks[idx], pos+i)
	}
}

func (d *Disk) String() string {
	s := make([]rune, len(d.blocks))
	for i, v := range d.blocks {
		if v >= 0 {
			s[i] = rune('0' + v)
		} else {
			s[i] = '.'
		}
	}
	return string(s)
}

func (d *Disk) leftmostGap(size int) *int {
	count := 0
	start := -1
	for i, v := range d.blocks {
		if v == -1 {
			if start == -1 {
				start = i
			}
			count++
			if count == size {
				return &start
			}
		} else {
			count = 0
			start = -1
		}
	}
	return nil
}

func (d *Disk) moveLeft(idx, pos, count int) {

	fileLen := len(d.fileBlocks[idx])
	if fileLen == 0 {
		return
	}
	lastBlock := d.fileBlocks[idx][fileLen-1]
	if pos > lastBlock {
		return
	}

	for i := 0; i < count; i++ {

		oidx := d.fileBlocks[idx][len(d.fileBlocks[idx])-1]
		d.fileBlocks[idx] = d.fileBlocks[idx][:len(d.fileBlocks[idx])-1]
		d.blocks[oidx] = -1

		d.blocks[pos+i] = idx
		d.fileBlocks[idx] = append([]int{pos + i}, d.fileBlocks[idx]...)
	}
}

type FileInfo struct {
	idx  int
	size int
}

func (d *Disk) revFiles() []FileInfo {
	idxs := make([]int, 0, len(d.fileBlocks))
	for idx := range d.fileBlocks {
		idxs = append(idxs, idx)
	}
	sort.Slice(idxs, func(i, j int) bool {
		return idxs[i] > idxs[j]
	})

	res := make([]FileInfo, 0, len(idxs))
	for _, idx := range idxs {
		res = append(res, FileInfo{idx, len(d.fileBlocks[idx])})
	}
	return res
}

func (d *Disk) checksum() int {
	sum := 0
	for i, v := range d.blocks {
		if v >= 0 {
			sum += i * v
		}
	}
	return sum
}

func sol1(data []int) int {
	D := NewDisk(data)
	for _, f := range D.revFiles() {
		for i := 0; i < f.size; i++ {
			g := D.leftmostGap(1)
			if g == nil {
				continue
			}
			D.moveLeft(f.idx, *g, 1)
		}
	}
	return D.checksum()
}

func sol2(data []int) int {
	D := NewDisk(data)
	for _, f := range D.revFiles() {
		g := D.leftmostGap(f.size)
		if g == nil {
			continue
		}
		D.moveLeft(f.idx, *g, f.size)
	}
	return D.checksum()
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	if !scanner.Scan() {
		return
	}
	line := scanner.Text()

	data := make([]int, 0, len(line))
	for _, ch := range line {
		n, err := strconv.Atoi(string(ch))
		if err != nil {
			continue
		}
		data = append(data, n)
	}

	fmt.Println(sol1(data))
	fmt.Println(sol2(data))
}
