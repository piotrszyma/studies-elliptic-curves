use num_bigint::BigUint;
use std::io;

fn step(
    value: &BigUint,
    alpha: &BigUint,
    beta: &BigUint,
    y: &BigUint,
    p: &BigUint,
    p_prim: &BigUint, 
    g_prim: &BigUint, 
) -> (BigUint, BigUint, BigUint) {
    // println!("value = {}", value);
    // println!("alpha = {}", alpha);
    // println!("beta = {}", beta);
    let res: BigUint = value % BigUint::from(3 as u8);
    if res == BigUint::from(1 as u8) {
        let new_beta = (beta + BigUint::from(1 as u8)) % p_prim;
        let new_value = (value * y) % p;
        (new_value, alpha.clone(), new_beta)
    } else if res == BigUint::from(0 as u8) {
        let new_alpha = (alpha * BigUint::from(2 as u8)) % p_prim;
        let new_beta = (beta * BigUint::from(2 as u8)) % p_prim;
        let new_value = (value * value) % p;
        (new_value, new_alpha, new_beta)
    } else if res == BigUint::from(2 as u8) {
        let new_alpha = (alpha + BigUint::from(1 as u8)) % p_prim;
        let new_value = (value * g_prim) % p;
        (new_value, new_alpha, beta.clone())
    } else {
        panic!("Value % 3 not in (0, 1, 2), something went wrong")
    }
}

fn run(g_prim: BigUint, p: BigUint, p_prim: BigUint, y: BigUint)  -> BigUint {
    println!("{}", g_prim);
    println!("{}", p);
    println!("{}", p_prim);
    println!("{}", y);

    let mut a = BigUint::from(1 as u8);
    let mut b = BigUint::from(1 as u8);

    let mut a_alpha = BigUint::from(0 as u8);
    let mut a_beta = BigUint::from(0 as u8);

    let mut b_alpha = BigUint::from(0 as u8);
    let mut b_beta = BigUint::from(0 as u8);

    loop {
        let result = step(&a, &a_alpha, &a_beta, &y, &p, &p_prim, &g_prim);
        a = result.0;
        a_alpha = result.1;
        a_beta = result.2;

        let result = step(&b, &b_alpha, &b_beta, &y, &p, &p_prim, &g_prim);
        b = result.0;
        b_alpha = result.1;
        b_beta = result.2;

        let result = step(&b, &b_alpha, &b_beta, &y, &p, &p_prim, &g_prim);
        b = result.0;
        b_alpha = result.1;
        b_beta = result.2;
        
        if a == b {
            break;
        }
    }

    // println!("a = {}", a);
    // println!("a_beta = {}", a_beta);
    // println!("b = {}", b);
    // println!("b_beta = {}", b_beta);

    let betas_diffs = a_beta - b_beta;
    let p_prim_less_two = &p_prim - BigUint::from(2 as u8);
    let beta_diffs_inv = betas_diffs.modpow(&p_prim, &p_prim_less_two);

    // println!("a_alpha = {}", &a_alpha % &p_prim);
    // println!("b_alpha = {}", &b_alpha % &p_prim);

    let alphas_diffs: BigUint = {
        if b_alpha < a_alpha {
            b_alpha + &p_prim - a_alpha
        } else {
            b_alpha - a_alpha
        }
    };
    let result = alphas_diffs * beta_diffs_inv;
    result % p_prim
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
