function run_ten_times {
  echo $1 $2" bits"
  for i in `seq 10`; do python3 -O  main.py --type $1 --path params_$2.json --value_to_find=3 --time_only; done

}

run_ten_times projective 20
run_ten_times affine 20
run_ten_times projective 40
run_ten_times affine 40
run_ten_times projective 60
run_ten_times affine 60
