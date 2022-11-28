#!/usr/bin/env bash

pandoc startctf.1.md -s -t man -o startctf.1

# Maybe compress the file here and include the gzip archive in the repo as well?