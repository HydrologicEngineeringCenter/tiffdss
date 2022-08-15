#!/bin/bash

pushd $(dirname $0)

python -m unittest discover -v -s ./tests/unit/
