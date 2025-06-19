#!/usr/bin/env bash
# publish.sh – bump a project’s version and tag the stable branch
set -euo pipefail

###############################################################################
# Defaults
###############################################################################
run=true            # --dry-run flips this to false
directory=""
branch_stable=stable
branch_dev=dev
commit_msg="General: Version bumped"
today=$(date +%F)   # YYYY-MM-DD
dirScript=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)

###############################################################################
# Option parsing
###############################################################################
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) run=false; shift ;;
    --stable)  shift; branch_stable=${1:?--stable needs a value}; shift ;;
    --dev)     shift; branch_dev=${1:?--dev needs a value}; shift ;;
    --msg)     shift; commit_msg=${1:?--msg needs a value}; shift ;;
    -h|--help)
      cat <<EOF
Usage: $0 [options] <directory>

Options
  --dry-run            Do everything except tag/commit/push
  --stable <branch>    Branch that receives the tag (default: stable)
  --dev <branch>       Development branch to return to (default: dev)
  --msg "<message>"    Commit message for the bump
  -h, --help           Show this help
EOF
      exit 0 ;;
    --*) echo "Unknown option: $1" >&2; exit 1 ;;
    *)
        echo "Unexpected extra argument: $1" >&2
        exit 1
  esac
done

###############################################################################
# Positional parameter: directory
###############################################################################
if [[ -z $dirScript ]]; then
  echo "Error: missing <directory>" >&2
  exit 1
fi

[[ $# -eq 0 ]] || { echo "Unexpected extra arguments: $*" >&2; exit 1; }

###############################################################################
# Read current version & optionally tag the stable branch
###############################################################################
current=$(<VERSION)

if $run; then
  echo "Tagging $branch_stable with $current …"
  git checkout "$branch_stable"
  git pull origin "$branch_stable"

  git tag "$current"
  git push origin "$current"

  git checkout "$branch_dev"
fi

###############################################################################
# Prompt for next version
###############################################################################
echo "Current version: $current"
read -rp "Enter new version: " version

echo "$version" > VERSION

###############################################################################
# Commit & push
###############################################################################
if $run; then
  git add VERSION
  git commit -m "$commit_msg to $version"
  git push origin "$branch_dev"
else
  echo "[dry-run] Would commit '$commit_msg to $version' and push to $branch_dev"
fi
