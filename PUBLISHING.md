# Publishing to PyPI

(Notes to self...)

Adapted from <https://realpython.com/pypi-publish-python-package/>

Python 3 only (from version 1.1.0 forward):

```
$ pip install twine
$ pip install 'readme_renderer[md]'
$ python setup.py sdist bdist_wheel
$ twine check dist/*
```

At this point, go to <https://test.pypi.org/> and ensure that the package
is there. If all looks good:

```
$ twine upload dist/*
```
