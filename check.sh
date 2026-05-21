#!/bin/sh
echo "-----  ty  -----"
ty check src
echo "----- ruff -----"
ruff check src
