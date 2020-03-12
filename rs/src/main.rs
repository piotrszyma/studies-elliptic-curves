use std::io;
use num_bigint::{BigUint};

const ZERO: BigUint= BigUint::from(0 as u8);
const ONE: BigUint = BigUint::from(0 as u8);
const TWO: BigUint = BigUint::from(0 as u8);
const THREE: BigUint = BigUint::from(3 as u8);

fn step(value: &BigUint, alpha: &BigUint, beta: &BigUint, y: &BigUint, p: &BigUint, g_prim: &BigUint) {
    match value % THREE {
        ZERO => {

        },
        ONE => {

        },
        TWO => {

        }
    }
}

fn pollard_rho_mpz(g_prim: BigUint, p: BigUint, p_prim: BigUint, y: BigUint) -> BigUint {
    println!("{}", g_prim);
    println!("{}", p);
    println!("{}", p_prim);
    println!("{}", y);

    let mut A = BigUint::from(1 as u8);
    let mut B = BigUint::from(1 as u8);

    let mut alphaA = BigUint::from(0 as u8);
    let mut betaA = BigUint::from(0 as u8);

    let mut alphaB = BigUint::from(0 as u8);
    let mut betaB = BigUint::from(0 as u8);

    loop {
        A = A;

        if A != B {
        break;
        }
    }

    alphaA + betaA
}

fn main() {
    let stdin = io::stdin();
    let mut input = String::new();

    stdin.read_line(&mut input).unwrap();
    let g_prim: BigUint = input.trim_end().parse().unwrap();
    println!("g_prim = {}", g_prim);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let p: BigUint = input.trim_end().parse().unwrap();
    println!("p = {}", p);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let p_prim: BigUint = input.trim_end().parse().unwrap();
    println!("p_prim = {}", p_prim);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let y: BigUint = input.trim_end().parse().unwrap();
    println!("y = {}", y);
    input.clear();

    pollard_rho_mpz(g_prim, p, p_prim, y);
}
