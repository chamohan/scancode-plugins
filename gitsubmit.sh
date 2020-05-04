#!/usr/bin/env bash

export GIT=`which git`
${GIT} add ${1}
${GIT} status
${GIT} commit ${1} 
${GIT} push origin master

