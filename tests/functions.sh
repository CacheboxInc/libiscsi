TGTD=tgtd
TGTADM=tgtadm
TGTLUN=`pwd`/100M
TGTPORTAL=127.0.0.1:3260

IQNTARGET=iqn.libiscsi.unittest.target
IQNINITIATOR=iqn.libiscsi.unittest.initiator
TGTURL=iscsi://${TGTPORTAL}/${IQNTARGET}/1

start_target() {
    # Setup target
    echo "Starting iSCSI target"
    ${TGTD} --iscsi portal=${TGTPORTAL},nop_interval=3,nop_count=3
    sleep 1
    ${TGTADM} --op new --mode target --tid 1 -T ${IQNTARGET}
    ${TGTADM} --op bind --mode target --tid 1 -I ALL
    #${TGTADM} --op show --mode target
}

shutdown_target() {
    # Remove target
    echo "Shutting down iSCSI target"
    ${TGTADM} --op delete --force --mode target --tid 1
    ${TGTADM} --op delete --mode system
}

create_lun() {
    # Setup LUN
    truncate --size=100M ${TGTLUN}
    ${TGTADM} --op new --mode logicalunit --tid 1 --lun 1 -b ${TGTLUN} --blocksize=4096
}

delete_lun() {
    # Remove LUN
    rm ${TGTLUN}
}

setup_chap() {
    ${TGTADM} --op new --mode account --user libiscsi --password libiscsi
    ${TGTADM} --op bind --mode account --tid 1 --user libiscsi

    ${TGTADM} --op new --mode account --user outgoing --password outgoing
    ${TGTADM} --op bind --mode account --tid 1 --user outgoing --outgoing
}

success() {
    echo "[OK]"
    rm ${TEST_TMP} 2> /dev/null
}

failure() {
    echo "[FAILED]"
    exit 1
}
