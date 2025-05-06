#!/bin/bash

set -e

ROOT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

if [[ ! -d _build/actions ]] ; then
   mkdir -p _build

   git clone https://github.com/syna-astra-dev/action-doc-publish.git ${ROOT_DIR}/_build/actions
fi

echo Building docker...

IMAGE_ID=$(docker build -q ${ROOT_DIR}/_build/actions/doc-build)

docker run --rm -e GITHUB_REF -v /:/host/ -w /host/${ROOT_DIR}/ ${IMAGE_ID}
