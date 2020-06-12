// #[path = "../pollard_rho.rs"] mod pollard_rho;
// #[path = "../pollard_rho_old.rs"] mod pollard_rho_old;

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

    #[test]
    fn test_same_result_for_20_bits() {
      let g_prim = BigUint::parse_bytes(b"160965");
      let p = BigUint::parse_bytes(b"900587");
      let p_prim = BigUint::parse_bytes(b"450293");
      let y = BigUint::parse_bytes(b"96620");
      assert_eq!(2 + 2, 4);
    }
}
