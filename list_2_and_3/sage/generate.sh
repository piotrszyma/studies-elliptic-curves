echo $1
docker run -v $(pwd):/home/sage/shared sagemath/sagemath:latest sage /home/sage/shared/ec-prime-order.sage $1
