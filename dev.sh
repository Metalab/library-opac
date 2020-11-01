#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

sourceRepo="https://github.com/Metalab/library-opac.git"
targetFolder="/var/www/html/sebastian/metalab-library-opac/branches"
sourceFolder="/var/www/html/sebastian/metalab-library-opac/source"

# If the repo is not present, clone it from github, otherwise do a git pull
if [ -d ${sourceFolder} ]; then
  echo "Repo is already cloned. Getting latest version..."
  cd ${sourceFolder}
  git pull
else
  echo "Repo is not clonded."
  git clone ${sourceRepo} ${sourceFolder}
fi

# For every branch, create a folder, delete the rest
rm -rf ${targetFolder}
mkdir ${targetFolder}

branches=$(git ls-remote --heads ${sourceRepo} | awk -F 'refs/heads/' '{print $2}')

for branch in "${branches[@]}"; do
  mkdir "${targetFolder}/${branch}"
  rsync -avP "${sourceFolder}/" "${targetFolder}/${branch}/"
  cd "${targetFolder}/${branch}"
  git checkout ${branch}
  cd ..
done
