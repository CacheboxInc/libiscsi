#!/bin/sh

. ./functions.sh

echo "WRITE 12"

echo -n "SCSI.Write12 ... "
../test-tool/iscsi-test-cu -i ${IQNINITIATOR} iscsi://${TGTPORTAL}/${IQNTARGET}/1 -t SCSI.Write12 --dataloss > /dev/null || failure
success

exit 0

