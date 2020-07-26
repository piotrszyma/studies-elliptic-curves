use num_bigint::BigUint;

fn step(
    value: u128,
    alpha: u128,
    beta: u128,
    y: u128,
    p: u128,
    p_prim: u128,
    g_prim: u128,
) -> (u128, u128, u128) {
    match (value % 3) {
        1 => {
            let new_beta = (beta + 1) % p_prim;
            let new_value = (value * y) % p;
            (new_value, alpha, new_beta)
        }
        0 => {
            let new_alpha = (alpha * 2) % p_prim;
            let new_beta = (beta * 2) % p_prim;
            let new_value = (value * value) % p;
            (new_value, new_alpha, new_beta)
        }
        2 => {
            let new_alpha = (alpha + 1) % p_prim;
            let new_value = (value * g_prim) % p;
            (new_value, new_alpha, beta)
        }
        _ => panic!("Value % 3 not in (0, 1, 2), something went wrong")
    }
}

pub fn run(g_prim: u128, p: u128, p_prim: u128, y: u128) -> u128 {
    dbg!(g_prim);
    dbg!(p);
    dbg!(p_prim);
    dbg!(y);

    let mut a = 1u128;
    let mut b = 1u128;

    let mut a_alpha = 0u128;
    let mut a_beta = 0u128;

    let mut b_alpha = 0u128;
    let mut b_beta = 0u128;

    loop {
        let result = step(a, a_alpha, a_beta, y, p, p_prim, g_prim);
        a = result.0;
        a_alpha = result.1;
        a_beta = result.2;

        let result = step(b, b_alpha, b_beta, y, p, p_prim, g_prim);
        b = result.0;
        b_alpha = result.1;
        b_beta = result.2;

        let result = step(b, b_alpha, b_beta, y, p, p_prim, g_prim);
        b = result.0;
        b_alpha = result.1;
        b_beta = result.2;
        
        if a == b {
            break;
        }
    }

    let betas_diffs = {
        if a_beta > b_beta {
            a_beta - b_beta
        } else {
            a_beta + p_prim - b_beta
        }
    };
    let p_prim_less_two = p_prim - 2;
    let beta_diffs_inv = (betas_diffs ^ p_prim) % p_prim_less_two;

    // println!("a_alpha = {}", &a_alpha % &p_prim);
    // println!("b_alpha = {}", &b_alpha % &p_prim);

    let alphas_diffs = {
        if b_alpha < a_alpha {
            b_alpha + p_prim - a_alpha
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
        let g_prim = 160965 as u128;
        let p = 900587 as u128;
        let p_prim = 450293 as u128;
        let y = 96620 as u128;

        // Act.
        let result = run(g_prim, p, p_prim, y);

        // Assert.
        assert_eq!(170878 as u128, result);
    }

    #[test]
    fn test_same_result_for_25_bits() {
        // Arrange.
        let g_prim = 14324026 as u128;
        let p = 30564299 as u128;
        let p_prim = 15282149 as u128;
        let y = 22392548 as u128;

        // Act.
        let result = run(g_prim, p, p_prim, y);

        // Assert.
        assert_eq!(3023260 as u128, result);
    }
}
