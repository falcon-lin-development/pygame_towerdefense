#! /bin/sh
activate() {
    source venv/bin/activate
}
remove_venv() {
    rm -rf ./venv
}

create_venv() {
    
    pip install virtualenv
    python3 -m virtualenv venv
    path_to_python=$(which python3)
    virtualenv -p $path_to_python venv
}

if [ -r "./venv/" ]; then
    activate
elif [ -d "./venv" ]; then
    remove_venv
    create_venv
    activate
else
    create_venv
    activate
fi

echo | which pip


