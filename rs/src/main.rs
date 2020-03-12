use num_bigint::BigUint;
use std::io;

fn step(
    value: &BigUint,
    alpha: &BigUint,
    beta: &BigUint,
    y: &BigUint,
    p: &BigUint,
    g_prim: &BigUint,
) -> () {
    let res: &BigUint = &(value % BigUint::from(3 as u8));

    if { res == &BigUint::from(0 as u8) } {
        let mut alpha = &(alpha  + BigUint::from(1 as u8));
        let mut value = &((value * y) % p);
    } else if { res == &BigUint::from(1 as u8) } {
        let mut alpha = &(alpha * BigUint::from(2 as u8));
        let mut beta = &(beta * BigUint::from(2 as u8));
        let mut value = &((value ^  BigUint::from(2 as u8)) % p);
    } else if { res == &BigUint::from(2 as u8) } {
        let mut beta = &(beta  + BigUint::from(1 as u8));
        let mut value = &((value * g_prim) % p);
    }
    return;
}

fn pollard_rho_mpz(g_prim: BigUint, p: BigUint, p_prim: BigUint, y: BigUint) {
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
        step(&A, &alphaA, &betaA, &y, &p, &g_prim);
        println!("{}", alphaA);
        step(&B, &alphaB, &betaB, &y, &p, &g_prim);
        step(&B, &alphaB, &betaB, &y, &p, &g_prim);
        if A != B {
            break;
        }
    }

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

    // pollard_rho_mpz(g_prim, p, p_prim, y);
}
