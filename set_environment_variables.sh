cat env-postgres.env | while read line; do
    echo $line
    export $line
done
