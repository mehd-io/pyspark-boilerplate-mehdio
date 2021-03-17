#!/usr/bin/env bash
mkdir to_upload
poetry export -f requirements.txt --output requirements.txt
pip3 -q install -r requirements.txt -t to_upload
cp -r {setup.py,datajob} to_upload
cd to_upload
version=$(echo `python3 setup.py --version` | sed s/_/-/g)
python3 setup.py sdist --format=zip
unzip -q "dist/datajob-$version.zip"
cd "datajob-$version"
# Small hack so that main package (datajob) can be added to python path
touch __init__.py
zip -q -r "../../datajob.zip" *
cd ../../
rm -r to_upload
