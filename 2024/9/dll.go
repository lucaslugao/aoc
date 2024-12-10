//go:build go_dll

package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

type Node struct {
	Pos, Idx, Size int
	Prev, Next     *Node
}

func (n *Node) End() int {
	return n.Pos + n.Size
}

func (n *Node) InsertAfter(node *Node) *Node {
	if n.Next != nil {
		n.Next.Prev = node
		node.Next = n.Next
	}
	n.Next = node
	node.Prev = n
	return n.Next
}

func (n *Node) InsertBefore(node *Node) *Node {
	if n.Prev != nil {
		n.Prev.Next = node
		node.Prev = n.Prev
	}
	n.Prev = node
	node.Next = n
	return n.Prev
}

func (n *Node) Remove() {
	if n.Prev != nil {
		n.Prev.Next = n.Next
	}
	if n.Next != nil {
		n.Next.Prev = n.Prev
	}
	n.Prev, n.Next = nil, nil
}

type Disk struct {
	GapHead    *Node
	Blocks     *Node
	BlocksTail *Node
	Index      map[int]*Node
}

func NewDisk(data []int) *Disk {
	d := &Disk{Index: make(map[int]*Node)}
	pos := 0

	for i := 0; i < len(data); i++ {
		if i%2 == 0 {
			bNode := &Node{Pos: pos, Idx: i / 2, Size: data[i]}
			d.Index[i/2] = bNode
			if d.Blocks == nil {
				d.GapHead = bNode
				d.Blocks = bNode
				d.BlocksTail = bNode
			} else {
				d.BlocksTail = d.BlocksTail.InsertAfter(bNode)
			}
			pos += data[i]
		} else {
			pos += data[i]
		}
	}
	return d
}

func (d *Disk) LeftmostGap(size int) *Node {
	if d.GapHead == nil || d.GapHead.Next == nil {
		return d.GapHead
	}
	for d.GapHead.Next != nil && d.GapHead.End() == d.GapHead.Next.Pos {
		d.GapHead = d.GapHead.Next
	}

	res := d.GapHead
	for res.Next != nil && res.Next.Pos-res.End() < size {
		res = res.Next
		if res.Next == nil {
			return nil
		}
	}
	return res
}

func (d *Disk) MoveLeft(idx int, node *Node, count int) {
	idxNode := d.Index[idx]
	if node.Pos >= idxNode.End() {
		return
	}
	idxNode.Size -= count
	if node.Idx == idx {
		node.Size += count
	} else {
		node.InsertAfter(&Node{Pos: node.End(), Idx: idx, Size: count})
	}
}

func (d *Disk) RevFiles() []struct{ Idx, Size int } {
	var result []struct{ Idx, Size int }
	for idx := range d.Index {
		result = append(result, struct{ Idx, Size int }{Idx: idx, Size: d.Index[idx].Size})
	}
	// Sort in descending order of index
	for i := 0; i < len(result)-1; i++ {
		for j := i + 1; j < len(result); j++ {
			if result[i].Idx < result[j].Idx {
				result[i], result[j] = result[j], result[i]
			}
		}
	}
	return result
}

func (d *Disk) String() string {
	var res []rune
	node := d.Blocks
	pos := 0
	for node != nil {
		for i := 0; i < node.Pos-pos; i++ {
			res = append(res, '.')
		}
		for i := 0; i < node.Size; i++ {
			res = append(res, rune('0'+node.Idx))
		}
		pos = node.End()
		node = node.Next
	}
	return string(res)
}

func (d *Disk) Checksum() int {
	check := 0
	node := d.Blocks
	for node != nil {
		check += (((2*node.Pos + node.Size - 1) * node.Size) / 2) * node.Idx
		node = node.Next
	}
	return check
}

func sol1(data []int) int {
	d := NewDisk(data)
	for _, file := range d.RevFiles() {
		idx, size := file.Idx, file.Size
		for i := 0; i < size; i++ {
			gap := d.LeftmostGap(1)
			if gap == nil {
				continue
			}
			d.MoveLeft(idx, gap, 1)
		}
	}
	return d.Checksum()
}

func sol2(data []int) int {
	d := NewDisk(data)
	for _, file := range d.RevFiles() {
		idx, size := file.Idx, file.Size
		gap := d.LeftmostGap(size)
		if gap == nil {
			continue
		}
		d.MoveLeft(idx, gap, size)
	}
	return d.Checksum()
}

func main() {
	scanner := bufio.NewScanner(os.Stdin)
	if scanner.Scan() {
		line := scanner.Text()
		data := make([]int, len(line))
		for i, c := range line {
			data[i], _ = strconv.Atoi(string(c))
		}
		fmt.Println(sol1(data))
		fmt.Println(sol2(data))
	}
}
