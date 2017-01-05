export PYTHONPATH=${PYTHONPATH}:~/"/git_repos/general_src/"
export PATH="${PATH}:/home/arubenstein/dist-packages/"
export PYTHONPATH="${PYTHONPATH}:/home/arubenstein/dist-packages/"
export PYTHONPATH=$PYTHONPATH:~/"/git_repos/deep_seq/"

#declare functions
check_file ()
{
        f=$1
        status=1
        if [[ -s $f ]]; then
            in=( $( < $f ) )
            if [[ $in != "0" ]]; then
                status=0
                echo "$1 has already been run"
            fi
        fi
        return $status
}

export -f check_file
