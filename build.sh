#!/bin/bash

if [[ "$1" == "private" ]]; then
  EXTRA_ARGS=true
fi

if [[ ! -d _build/actions ]] ; then
   mkdir -p _build

   git clone org-150332546@github.com:syna-astra-dev/actions.git _build/actions
fi

docker build -t actions/build-sphinx _build/actions/build-sphinx

docker run --rm -it -v $(pwd):$(pwd) -u $(id -u):$(id -g) actions/build-sphinx $(pwd) $(pwd)/_build ${EXTRA_ARGS}
