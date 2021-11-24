@echo off

set tagname=%1
set message=%2

echo %message%

git tag -a %tagname% -m "%message%"
git push origin %tagname%