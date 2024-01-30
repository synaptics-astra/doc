#!/bin/bash

if [[ "$1" == "private" ]]; then
  EXTRA_ARGS=true
fi

docker build -t actions/build-sphinx .github/actions/build-sphinx

docker run --rm -it -v $(pwd):$(pwd) -u $(id -u):$(id -g) actions/build-sphinx $(pwd) $(pwd)/_build ${EXTRA_ARGS}
