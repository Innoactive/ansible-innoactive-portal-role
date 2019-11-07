import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_media_storage_is_mounted_on_host(host):
    mount_point = "/mnt/hub-media-storage"
    assert host.mount_point(mount_point).exists
    assert host.file("%s/test.txt" % mount_point).exists
