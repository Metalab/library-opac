#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

set -e

sourceRepo="https://github.com/Metalab/library-opac.git"
targetFolder="/var/www/html/sebastian/metalab-library-opac/branches"
sourceFolder="/var/www/html/sebastian/metalab-library-opac/source"

sudo apt-get install -y golang-go rsync minify npm > /dev/null
export GOPATH=/tmp/go && go get github.com/Clever/csvlint/cmd/csvlint

# If the repo is not present, clone it from github, otherwise do a git pull
if [ -d ${sourceFolder} ]; then
  echo "Repo is already cloned. Getting latest version..."
  cd ${sourceFolder}
  git pull
  ./update.sh
else
  echo "Repo is not cloned."
  git clone ${sourceRepo} ${sourceFolder}
  cd ${sourceFolder}
  ./update.sh
fi

/tmp/go/bin/csvlint /tmp/library-media-inventory/inventory.csv

# For every branch, create a folder, delete the rest
rm -rf ${targetFolder}
mkdir ${targetFolder}

git ls-remote --heads ${sourceRepo} | awk -F 'refs/heads/' '{print $2}' > /tmp/branches

for branch in $(< /tmp/branches); do
  mkdir ${targetFolder}/${branch}
  rsync -avP "${sourceFolder}/" "${targetFolder}/${branch}/"
  cd ${targetFolder}/${branch}
  git checkout ${branch}

  if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt > /dev/null
    npm install
    rsync -av --info=progress2 --delete ./static/ ./upload/
    ./staticSiteGenerator.py
  fi
  cd ..
done
