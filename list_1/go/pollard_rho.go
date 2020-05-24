package main

import (
	"fmt"
	"math/big"
)

type PollardRho struct {
	g_prim *big.Int
	p      *big.Int
	p_prim *big.Int
	y      *big.Int
}

func (pollard_rho PollardRho) String() string {
	return fmt.Sprintf("PollardRho g_prim: %d p: %d p_prim: %d y: %d", pollard_rho.g_prim, pollard_rho.p, pollard_rho.p_prim, pollard_rho.y)
}

type Point struct {
	alpha *big.Int
	beta  *big.Int
}

func (point *Point) String() string {
	return fmt.Sprintf("Point alpha: %d beta: %d", point.alpha, point.beta)
}

func createPoint() *Point {
	return &Point{
		alpha: big.NewInt(1),
		beta:  big.NewInt(1),
	}
}

func (pollard *PollardRho) step(value *big.Int, poeValue *Point) {
	var mod big.Int

	mod = *mod.Mod(value, big.NewInt(3))

	if mod.Cmp(new(big.Int).SetInt64(1)) == 0 {
		poeValue.beta = poeValue.beta.Add(poeValue.beta, big.NewInt(1))
		poeValue.beta = poeValue.beta.Mod(poeValue.beta, pollard.p_prim)
		value = value.Mul(value, pollard.y)
		value = value.Mod(value, pollard.p)
	} else if mod.Cmp(new(big.Int).SetInt64(0)) == 0 {
		poeValue.alpha = poeValue.alpha.Mul(poeValue.alpha, big.NewInt(2))
		poeValue.alpha = poeValue.alpha.Mod(poeValue.alpha, pollard.p_prim)
		poeValue.beta = poeValue.beta.Mul(poeValue.beta, big.NewInt(2))
		poeValue.beta = poeValue.beta.Mod(poeValue.beta, pollard.p_prim)
	} else { // if mod.Cmp(new(big.Int).SetInt64(0)) == 0
		poeValue.alpha = poeValue.alpha.Add(poeValue.alpha, big.NewInt(1))
		poeValue.alpha = poeValue.alpha.Mod(poeValue.alpha, pollard.p_prim)
		value = value.Mul(value, pollard.g_prim)
		value = value.Mod(value, pollard.p)
	}
	fmt.Println("in: ", value)
}

func (pollard *PollardRho) walk() *big.Int {
	A := big.NewInt(1)
	B := big.NewInt(1)
	poeA := createPoint()
	poeB := createPoint()

	for {
		pollard.step(A, poeA)
		fmt.Println("out: ", A)
		pollard.step(B, poeB)
		fmt.Println("out: ", B)
		pollard.step(B, poeB)
		fmt.Println("out: ", B)
		// fmt.Println("A:", A)
		// fmt.Println("poeA:", poeA)
		// fmt.Println("B:", B)
		// fmt.Println("poeB:", poeB)

		if A == B {
			break
		}
	}

	return big.NewInt(1)
}

func (pollard *PollardRho) Run() *big.Int {
	fmt.Println("Starting walk")
	return pollard.walk()
}
