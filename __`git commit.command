cd "$(dirname "$0")"

git add .
git commit -am "$*"
git push origin -fu main
