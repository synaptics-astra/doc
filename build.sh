#!/bin/bash

docker build -t actions/build-sphinx .github/actions/build-sphinx

docker run --rm -it -v $(pwd):$(pwd) -u $(id -u):$(id -g) actions/build-sphinx $(pwd) $(pwd)/_build