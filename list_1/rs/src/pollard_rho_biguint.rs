use num_bigint::BigUint;

fn step(
    value: &BigUint,
    alpha: &BigUint,
    beta: &BigUint,
    y: &BigUint,
    p: &BigUint,
    p_prim: &BigUint,
    g_prim: &BigUint,
) -> (BigUint, BigUint, BigUint) {
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

pub fn run(g_prim: BigUint, p: BigUint, p_prim: BigUint, y: BigUint) -> BigUint {
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

    let betas_diffs = {
        if a_beta > b_beta {
            a_beta - b_beta
        } else {
            a_beta + &p_prim - b_beta
        }
    };
    let p_prim_less_two = &p_prim - BigUint::from(2 as u8);
    // dbg!(&betas_diffs);
    // dbg!(&p_prim);
    // dbg!(&p_prim_less_two);
    let beta_diffs_inv = betas_diffs.modpow(&p_prim, &p_prim_less_two);
    dbg!(&beta_diffs_inv);

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
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_same_result_for_20_bits() {
        // Arrange.
        let g_prim = BigUint::parse_bytes(b"160965", 10).unwrap();
        let p = BigUint::parse_bytes(b"900587", 10).unwrap();
        let p_prim = BigUint::parse_bytes(b"450293", 10).unwrap();
        let y = BigUint::parse_bytes(b"96620", 10).unwrap();

        // Act.
        let result = run(g_prim, p, p_prim, y);

        // Assert.
        assert_eq!(BigUint::parse_bytes(b"170878", 10).unwrap(), result);
    }

    #[test]
    fn test_same_result_for_25_bits() {
        // Arrange.
        let g_prim = BigUint::parse_bytes(b"14324026", 10).unwrap();
        let p = BigUint::parse_bytes(b"30564299", 10).unwrap();
        let p_prim = BigUint::parse_bytes(b"15282149", 10).unwrap();
        let y = BigUint::parse_bytes(b"22392548", 10).unwrap();

        // Act.
        let result = run(g_prim, p, p_prim, y);

        // Assert.
        assert_eq!(BigUint::parse_bytes(b"3023260", 10).unwrap(), result);
    }

    #[test]
    #[ignore]
    fn test_same_result_for_40_bits() {
        // Arrange.
        let g_prim = BigUint::parse_bytes(b"550859632345", 10).unwrap();
        let p = BigUint::parse_bytes(b"944112437267", 10).unwrap();
        let p_prim = BigUint::parse_bytes(b"472056218633", 10).unwrap();
        let y = BigUint::parse_bytes(b"19459354526", 10).unwrap();

        // Act.
        let result = run(g_prim, p, p_prim, y);

        // Assert.
        assert_eq!(BigUint::parse_bytes(b"320531016627", 10).unwrap(), result);
    }
}
