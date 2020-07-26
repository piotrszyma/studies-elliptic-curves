use num_bigint::BigUint;
use std::io;

mod pollard_rho;
mod pollard_rho_biguint;

fn main() {
    let stdin = io::stdin();
    let mut input = String::new();

    stdin.read_line(&mut input).unwrap();
    let g_prim: u128 = input.trim_end().parse().unwrap();
    println!("g_prim = {}", g_prim);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let p: u128 = input.trim_end().parse().unwrap();
    println!("p = {}", p);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let p_prim: u128 = input.trim_end().parse().unwrap();
    println!("p_prim = {}", p_prim);
    input.clear();

    stdin.read_line(&mut input).unwrap();
    let y: u128 = input.trim_end().parse().unwrap();
    println!("y = {}", y);
    input.clear();

    let result = pollard_rho::run(g_prim, p, p_prim, y);

    println!("result = {}", result)
}
