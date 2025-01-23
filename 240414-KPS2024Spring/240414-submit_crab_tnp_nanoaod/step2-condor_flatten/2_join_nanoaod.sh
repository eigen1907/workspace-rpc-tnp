#!/bin/bash
cmsenv
for dir in *
do
    if [ -d ${dir} ]
        then hadd ${dir}/$(basename ${dir}).root ${dir}/output/*.root
    fi
done
