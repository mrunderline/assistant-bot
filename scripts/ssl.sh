#!/bin/bash

website="$1"
certificate_file=$(mktemp)
echo -n | openssl s_client -servername "$website" -connect "$website":443 2>/dev/null | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' >$certificate_file
date=$(openssl x509 -in $certificate_file -enddate -noout | sed "s/.*=\(.*\)/\1/")
date_s=$(date -d "${date}" +%s)
now_s=$(date -d now +%s)
date_diff=$(((date_s - now_s) / 86400))
echo "$website will expire in $date_diff days"
rm "$certificate_file"
