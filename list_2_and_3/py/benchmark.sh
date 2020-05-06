echo "projective 20 bits"
for i in `seq 10`; do python3 -O  main.py --type projective --path params_20.json --value_to_find=3 --time_only; done

echo "affine 20 bits"
for i in `seq 10`; do python3 -O  main.py --type affine --path params_20.json --value_to_find=3 --time_only; done
