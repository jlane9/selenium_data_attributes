#!/bin/bash



filename=
while [ $# -gt 0 ]
do
    case "$1" in
        -v)  VERSION=$2;;
	-g)  filename="$2"; shift;;
	--)	shift; break;;
	-*)
	    echo >&2 \
	    "usage: $0 [-v] [-f file] [file ...]"
	    exit 1;;
	*)  break;;	# terminate while loop
    esac
    shift
done


# Navigate to SDA path
cd $HOME/selenium_data_attributes/

# Update versions on files
sed -i '' -E -- "s/__version__ = '.*'/__version__ = '$VERSION'/g" sda/*.py
sed -i '' -E -- "s/version='.*'/version='$VERSION'/g" setup.py
sed -i '' -E -- "s/download_url='.*'/download_url='https:\/\/github.com\/jlane9\/selenium-data-attributes\/tarball\/$VERSION'/g" setup.py

# Update source for GitHub
git add --all
git commit -m "$VERSION release"

# Add GitHub release tag
git tag ${VERSION} -m "PyPi release $VERSION"
git push --tags origin master

python setup.py sdist bdist_wheel upload -r "https://pypi.python.org/pypi"

echo "${VERSION} released..."




















