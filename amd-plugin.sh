export GIT=`which git`
export PIP=`which pip`

${GIT} clone https://github.com/chamohan/scancode-plugins.git
${PIP} install -e scancode-plugins/scancode-keywords-scan/
${PIP} install -e scancode-plugins/scancode-licence-modifications/
${PIP} install -e scancode-plugins/scancode-no-licenses/
{$PIP} install -e scancode-plugins/scancode-only-licenses-titles}/
