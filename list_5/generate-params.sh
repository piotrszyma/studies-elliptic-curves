DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run -v $DIR:/home/sage/shared sagemath/sagemath:latest sage /home/sage/shared/generate-params.sage $1 | tail -n  1
