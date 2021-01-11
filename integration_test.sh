#!/bin/bash

getopt --test > /dev/null
if [[ $? != 4 ]]; then
    echo "I’m sorry, `getopt --test` failed in this environment."
    exit 1
fi
EXE=${0##*/}

help=false
insecure=false
host=https://localhost:5000
plaintext="foo bar azang zving"
print_usage () {
    echo "    $EXE [-h|--help] [-k|--insecure] [-a|--addr <http-address>] [-i|--input <input-string>]"
    echo "          -h|--help (print usage)"
    echo "          -k|--insecure (make curl accept insecure https certificates - dev only)"
    echo "          -a|--addr <http-address> (default: $host)"
    echo "          -i|--input <input-string> (default: $plaintext)"
}


SHORT=hka:i:
LONG=help,insecure,addr:,input:
PARSED=`getopt --options $SHORT --longoptions $LONG --name "$0" -- "$@"`
if [[ $? != 0 ]]; then
    exit 2
fi
eval set -- "$PARSED"

while true; do
    case "$1" in
        -h|--help)
            help=true
            shift
            ;;
        -k|--insecure)
            insecure=true
            shift
            ;;
        -a|--addr)
            host="$2"
            shift 2
            ;;
        -i|--input)
            plaintext="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Parsing error"
            exit 3
            ;;
    esac
done

if [ $help == "true" ]; then
    print_usage
    exit 0
fi

curl="curl"
if [ $insecure == "true" ]; then
    curl="curl -k"
fi

response=`$curl --header "Content-Type: application/json" --request POST --data '{"data":"'"$plaintext"'"}' $host/oracleinvocation`

key=`echo $response | jq -r '.key'`
data=`echo $response | jq -r '.data'`
mac=`echo $response | jq -r '.mac'`
nonce=`echo $response | jq -r '.nonce'`
# echo $data $key $mac $nonce

decodedtext=`python3 decode_cli.py "$key" "$data" "$mac" "$nonce"`
echo $plaintext
echo $decodedtext

if [[ "$plaintext" == "$decodedtext" ]]; then
   echo "Test passed."
   exit 0
else
   echo "Test FAILED!"
   exit 1
fi
