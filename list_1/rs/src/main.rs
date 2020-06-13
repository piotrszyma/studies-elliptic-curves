use num_bigint::BigUint;
use std::io;

mod pollard_rho_old;

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

    let result = pollard_rho_old::run(g_prim, p, p_prim, y);

    println!("result = {}", result)
}
