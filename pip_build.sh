[ -d build ] && rm -fr build
[ -d dist ] && rm -fr dist
[ -d kdic.egg-info ] && rm -fr kdic.egg-info
python3 setup.py sdist bdist_wheel
echo "Test"
sleep 1
tar tzf dist/*.tar.gz
twine check dist/*
#python -m build
# Install
#python -m pip install dist/xxx.whl
