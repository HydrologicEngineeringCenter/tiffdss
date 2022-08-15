#!/bin/bash

# Set directory stack to this script's directory
pushd $(dirname $0)

usage(){
    printf "\n$0 Usage:\n" && grep " .)\ #" $0
    exit 0;
}

options=":hc:m:t:"
while getopts  $options option
do
    case $option in
        c   ) # Class name
                class=$OPTARG
                ;;
        m   ) # Method in class
                method=$OPTARG
                ;;
        t   ) # Test script
                test_script=$OPTARG
                ;;
        h   ) # Display Usage
                usage
                ;;
        \?  ) # Unknown option
                printf "\nUnknown option: -$OPTARG\n" >&2
                exit 1;;
        :   ) # Missing option argument
                printf "\nMissing option argument for -$OPTARG\n" >&2
                exit 1;;
        *   ) # Unimplemented option
                printf "\nUnimplemented option: -$option\n" >&2
                exit 1;;
    esac
done

if [ -z $test_script ] || [ -z $method ] || [ -z $class ]; then
    printf "\nCheck for missing script, class, or method\n"
    usage
fi

python -m unittest ${test_script}.${class}.${method}
