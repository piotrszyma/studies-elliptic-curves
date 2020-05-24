package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
	"strings"
)

func read_number(reader *bufio.Reader) *big.Int {
	value, _ := reader.ReadString('\n')
	num, _ := new(big.Int).SetString(strings.TrimSpace(value), 10)
	return num
}

func main() {
	reader := bufio.NewReader(os.Stdin)

	g_prim := read_number(reader)
	p := read_number(reader)
	p_prim := read_number(reader)
	y := read_number(reader)

	pollard_rho := PollardRho{
		g_prim: g_prim,
		p:      p,
		p_prim: p_prim,
		y:      y,
	}

	fmt.Println("Running for:", pollard_rho)
	// result := pollard_rho.Run()
	// fmt.Println(result)

	var source = big.NewInt(10)
	var mod big.Int

	mod.Mod(source, big.NewInt(3))
	fmt.Println(mod)
	// result := new(big.Int).SetInt64(3)

}
