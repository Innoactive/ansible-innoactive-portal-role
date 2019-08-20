import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_is_docker_installed(host):
    package_docker = host.package('docker-ce')

    assert package_docker.is_installed


def test_docker_python_package_installed(host):
    pip_package_docker = host.pip_package.get_packages().get('docker')

    assert pip_package_docker


def test_services_are_running(host):
    stack_prefix = 'molecule_test_hub_'

    with host.sudo():
        expected_service_names = [service_name % stack_prefix for
                                  service_name in [
                                      "%sweb",
                                      "%schannels",
                                      "%snginx",
                                      "%snginx_gen",
                                      "%smq",
                                      "%sdb",
                                      "%sportal",
                                      # "%shub_fluentd"
                                  ]]
        actual_service_names = [container.name for container in
                                host.docker.get_containers(status="running")]
        for expected_service_name in expected_service_names:
            assert expected_service_name in actual_service_names

# TODO: test that channels container (websocket) is running and accepts
# connections (channels is connected to via http)
# TODO: test that an oauth client exists for the portal (with redirect
# uri specified)
