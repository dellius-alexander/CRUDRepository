#!/bin/bash
VERSION=$(cat "VERSION")
rm -rf dist/** && \
rm -rf build/**

# update version in pyproject.toml
sed -E "s/version[[:space:]]*=[[:space:]]*\"[0-9]+\.[0-9]+\.[0-9]+\"/version = \"${VERSION}\"/g" pyproject.toml | tee pyproject-temp.toml

# update version in pyproject.toml
if mv pyproject-temp.toml pyproject.toml ; then
    echo "Successfully updated version in pyproject.toml"
    rm -rf pyproject-temp.toml
else
    echo "Failed to update version in pyproject.toml"
    exit 1
fi

exit 0

# install setuptools and wheel
if python3 -m pip install --upgrade setuptools wheel twine 2>&1 ; then
    echo "Successfully installed setuptools and wheel"
else
    echo "Failed to install setuptools and wheel"
    exit 1
fi

# install requirements
if python3 -m pip install -r requirements.txt 2>&1 ; then
    echo "Successfully installed requirements"
else
    echo "Failed to install requirements"
    exit 1
fi

# run tests
if python3 -m pytest tests/ 2>&1 ; then
    echo "Testsing completed Successfully."
else
    echo "Tests failed to complete successfully."
    exit 1
fi

#  build
if python3 -m build 2>&1 ; then
    echo "Build and test ran Successfully."
else
    echo "Build failed to complete successfully."
    exit 1
fi

# upload to pypi
python3 -m twine upload \
--config-file .pypirc \
dist/* --verbose --skip-existing &>/dev/null
