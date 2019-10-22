import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_samba_service_is_running(host):
    samba = host.service("smbd")
    assert samba.is_running
    assert samba.is_enabled


def test_samba_fileshare_is_mounted_on_host(host):
    mount_point = "/mnt/hub-media-storage"
    assert host.mount_point(mount_point).exists
    assert host.file("%s/test.txt" % mount_point).exists
