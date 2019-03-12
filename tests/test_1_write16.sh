#!/bin/sh

. ./functions.sh

echo "WRITE 16"

echo -n "SCSI.Write16 ... "
../test-tool/iscsi-test-cu -i ${IQNINITIATOR} iscsi://${TGTPORTAL}/${IQNTARGET}/1 -t SCSI.Write16 --dataloss > /dev/null || failure
success

exit 0

