virtualenv --system-site-packages --python=python2.7 venv/pyvenv
source venv/pyvenv/bin/activate
pip install -r venv/requirements.txt

#
# for this project you will also need NodeJS for tooling
# here's instructions for installing on CentOS 6.4
#
https://gist.github.com/neojp/5561946

#
#  after node is installed, install dependencies
#
npm install # it will read package.json

#
#  then run  make file to build JavaScript
#
make
