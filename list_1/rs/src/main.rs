use mod_exp::mod_exp;
use std::io;
use std::time::{Duration, Instant};


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

    // dbg!(g_prim);
    // dbg!(p);
    // dbg!(p_prim);
    // dbg!(y);

    let x_found = pollard_rho::run(g_prim, p, p_prim, y);

    // Assert.
    let start = Instant::now();
    let y_calculated = mod_exp(g_prim, x_found, p);
    println!("Found in {} ns", start.elapsed().as_nanos());

    assert_eq!(y, y_calculated);

    println!("x_found = {}", x_found)
}
