#!/bin/sh
set -e

notebook_dir=$1

cd $notebook_dir

ERRORS=""

# convert py files to notebooks
for file in 20*.py
do
    if jupytext -o "${file%.*}.ipynb" "${file%.*}.py"; then
        echo "Sucessfully converted ${file}\n\n\n\n"
        git add "${file}"
    else
        echo "ERROR Converting ${file}"
        ERRORS="${ERRORS}, ${file}"
    fi
done

# run all notebooks
for file in *.ipynb
do
    if papermill --kernel python3 "${file}" "${file}"; then
        echo "Sucessfully refreshed ${file}\n\n\n\n"
    else
        echo "ERROR Refreshing ${file}"
        ERRORS="${ERRORS}, ${file}"
    fi
done

# Emit Errors If Exists So Downstream Task Can Open An Issue
if [ -z "$ERRORS" ]
then
    echo "::set-output name=error_bool::false"
else
    echo "These files failed to update properly: ${ERRORS}"
    echo "::set-output name=error_bool::true"
    echo "::set-output name=error_str::${ERRORS}"
fi
