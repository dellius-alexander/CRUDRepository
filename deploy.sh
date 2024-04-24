#!/bin/bash
VERSION=$(cat VERSION)
rm -rf dist/** && \
sed -e "s/version = \"[[:digit:]]\.[[:digit:]]\.[[:digit:]]\"/version = \"${VERSION}\"/g" setup.py | tee setup.temp.py && \
sed -e "s/version = \"[[:digit:]]\.[[:digit:]]\.[[:digit:]]\"/version = \"${VERSION}\"/g" setup.cfg | tee setup.temp.cfg && \
exit 0
mv setup.temp.py setup.py && \
mv setup.temp.cfg setup.cfg && \
mv src/utils/parsers/args_parser.temp.py src/utils/parsers/args_parser.py && wait $!

if python3 -m pytest tests/ 2>&1 ; then
    echo "Testsing completed Successfully."
else
    echo "Tests failed to complete successfully."
    exit 1
fi

if poetry build 2>&1 ; then
    echo "Build and test ran Successfully."
else
    echo "Build failed to complete successfully."
    exit 1
fi

#python3 -m twine upload dist/* --verbose --skip-existing --
#python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* --verbose --skip-existing
#if python3 -m pip install src 2>&1 ; then
#    echo "Successfully installed the package"
#else
#    echo "Failed to install the package"
#fi