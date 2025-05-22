#!/bin/bash

set -e

ROOT_DIR=$(dirname $(readlink -f ${BASH_SOURCE[0]}))

docker run -e GITHUB_REF -e GITHUB_REPOSITORY --rm -v /:/host/ -w /host/${ROOT_DIR}/ ghcr.io/syna-astra-dev/synaptics-sphinx-theme/builder:latest
