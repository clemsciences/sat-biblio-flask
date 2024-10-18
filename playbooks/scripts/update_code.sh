#!/bin/bash
git stash
git checkout master
git pull
git checkout prod
git rebase master
git stash pop