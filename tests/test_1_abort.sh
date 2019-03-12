#!/bin/sh

. ./functions.sh

echo "ABORT - TASK MANAGEMENT FUNCTION TEST"

#python3 ./utils/tgt_crash_test.py
echo -n "../test-tool/iscsi-test-cu -i ${IQNINITIATOR} iscsi://${TGTPORTAL}/${IQNTARGET}/1 -t SCSI.iSCSITMF --dataloss"
../test-tool/iscsi-test-cu -i ${IQNINITIATOR} iscsi://${TGTPORTAL}/${IQNTARGET}/1 -t SCSI.iSCSITMF --dataloss || failure
success

#shutdown_target
#python3 ./utils/tgt_cleanup.py

exit 0
