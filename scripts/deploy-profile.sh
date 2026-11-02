# App-owned publication contract; common engine: BaseCentral deploy 1.0.0.
APP_ID=verbal
SOURCE_SUBDIR=public
DEFAULT_DESTINATION="${DEPLOY_SITE:-$HOME/verbal.basecentral.link}"
DEPLOY_URL=https://verbal.basecentral.link
PUBLIC_FILES=$(cat <<'PUBLIC_FILES'
index.html
style.css
paper.css
paper-data.js
paper.js
words.js
guesses.js
dictionary-license.txt
english.js
english-license.txt
vocabulary.js
paper-en-data.js
core.js
challenges.js
variants.js
i18n.js
app.js
manifest.webmanifest
icon.svg
icon-192.png
icon-512.png
flag-pt.svg
flag-en.svg
shared-controls.css
shared-icons.svg
shared-chevron.svg
release.json
sw.js
PUBLIC_FILES
)
deploy_validate(){
  local hash rel listed
  listed=$(cut -d ' ' -f2- "$DEPLOY_CHECKOUT/scripts/deploy-hashes.txt" | sort)
  [[ "$listed" == "$(printf '%s\n' "$PUBLIC_FILES" | sort)" ]] || deploy_fail 'Deployment checksum inventory does not exactly match public files.'
  while read -r hash rel;do [[ "$(deploy_sha "$1/$rel")" == "$hash" ]] || deploy_fail "Release digest mismatch: $rel";done < "$DEPLOY_CHECKOUT/scripts/deploy-hashes.txt"
}
deploy_validate_stage(){ deploy_validate "$1"; }
