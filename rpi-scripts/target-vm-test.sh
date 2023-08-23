
function ping_test () {
    timeout 1s ping -c 1 10.0.0.4 &&
    timeout 1s ping -c 1 10.0.0.5 &&
    timeout 1s ping -c 1 10.0.0.6 &&
    timeout 1s ping -c 1 10.0.0.7 &&
    echo "passed $(date)"
    return $?
}

while true; do
    # api: restart bp
    echo -n "API restart bp: "
    curl http://recolic-home.freemyip.com:30401/trigger
    date >> tests.log
    sleep 7
    ping_test && continue
    sleep 10 # wait for second try
    ping_test && continue
    sleep 10 # wait for second try
    ping_test && continue
    sleep 60 # wait for second try
    ping_test && continue
    sleep 10 # wait for second try
    ping_test && continue
    echo "REPRO!!"
    break
done


