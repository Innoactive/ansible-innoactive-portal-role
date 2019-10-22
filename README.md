# Role Name

This role sets up a host to run the Innoactive Hub - XR platform.

## Requirements

Since the deployment uses [json_query](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter)
to extract important values from json data structures, the respective pip package [jmespath](http://jmespath.org/) needs
to be installed locally via pip.

Also, the Innoactive Hub's images are distributed via Innoactive's private Docker registry so in order to access and deploy
them, credentials to access the docker registry at `registry.docker.innoactive.de` are required.

## Installation

To install this role locally, simply run `ansible-galaxy install git+git@github.com:Innoactive/ansible-innoactive-hub-role.git`.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

### Docker Registry

    registry_hostname: registry.docker.innoactive.de

The registry from which to pull images of the Hub's containers.

    registry_username:

The username to use to authenticate against the specified docker registry.

    registry_password:

The password to use to authenticate against the specified docker registry.

### Innoactive Hub

    hostname:

The hostname under which the Hub instance will be available (this needs to be publicly reachable).

    secret_key:

A user-defined, secret key used for salting hashes within the Hub's application. Never expose this to anyone!

    admin_email:

E-Mail address of the main admin user, used to notify upon errors, expired certificates, etc.

    admin_password:

Password of the main admin user to login to the Hub instance and manage other users or content.

    create_admin_user: true

Whether to ensure the creation of an admin user on the Hub instance, may be skipped if users are setup manually.

    setup_database: true

Whether to run database migrations and setup the database.

    setup_wmc: true

Whether to make the static frontend assets available on the Hub instance (styles, images, scripts). I.e. setup the frontend.

    sentry_dsn:

DSN for [Sentry](https://sentry.io/welcome/) to automatically track runtime errors.

    google_analytics_tracking_id:

Tracking ID of a Google Analytics Property to monitor usage of the Hub.

#### Media Files

The Hub's files (user uploads like applications, assets, ...) are stored within a dedicated docker volume. To ensure
sufficient space, backing this volume with an external storage via cifs or a locally mounted disk can make sense.
To enable the volume storage for media files, we need to decide whether to use the local or cifs mount options and
specify those accordingly:

##### CIFS

To go for a CIFS mounted volume for the media files, the following needs to be specified

    media_volume_mount:
      cifs:
        url:
        username:
        password:

The individual values of the configuration object are explained below:

    url:

The public URL of the storage / file share supporting CIFS.

    username:

The username to use for authentication against the CIFS file share.

    password:

The password to use for authentication against the CIFS file share.

##### Local Mount / Drive

As an alternative to the Samba / CIFS share, we can also use a local disk, drive or folder for the static files, as long
as the filesystem on this mountpoint is `ext4`. To make use of it, we need to configure as follows:

    media_volume_mount:
      local:
        path:

with:

    path:

An absolute path on the filesystem pointing to an `ext4`-formatted volume / storage.

#### Versioning

It is possible to deploy different versions of the Innoactive Hub's services by specifying the following variables.
Available versions for the docker container images can be found in our registry at `registry.docker.innoactive.de`.

    portal_image_version: latest

The version of the Innoactive Hub's Portal container.

    hub_image_version: latest

The version of the Innoactive Hub's Main Service container.

    reverse_proxy_image_version: 1.2.1

The version of the reverse proxy image to be used.

### Secured Communication

    letsencrypt: true

Whether or not to use [Let's Encrypt](https://letsencrypt.org/) to issue SSL / TLS certificates. Set this to false if
you intend to use custom certificates or no certificates at all.

    letsencrypt_test: false

When using [Let's Encrypt](https://letsencrypt.org/) to issue SSL / TLS certificates this flag (defaults to false) can be
used to issue certificates by Let's Encrypt's [staging environment](https://letsencrypt.org/docs/staging-environment/)
instead of the production environment.

### Innoactive Discovery Portal

    portal_hostname: "portal.{{ hub_configuration.hostname  }}"

The hostname under which the discovery portal should be publicly availabe. This defaults to `portal.<hostname-of-hub-instance>`.

    portal_oauth_client_id:

Allows to explicitly define the oauth client id to be used by the portal to communicate with the Hub. If not defined,
an oauth client will automatically be retrieved.

    portal_oauth_client_secret:

Allows to explicitly define the oauth client secret to be used by the portal to communicate with the Hub. If not defined,
an oauth client will automatically be retrieved.

### Mail Setup

    gmail_user:

Username / E-Mail for a G-Mail account that can be used to send out emails.

    gmail_password:

Password for the specified G-Mail account.

## Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set
for other roles, or variables that are used from other roles.

- [geerlingguy.pip](https://github.com/geerlingguy/ansible-role-pip)

If the server to which to apply the Innoactive Hub role to does not come with docker pre-installed, it is helpful to also
use:

- [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker)

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for
users too:

    - hosts: servers
      roles:
        - role: geerlingguy.docker
          become: true
        - role: innoactive.hub
          vars:
            # main configuration parameters
            registry_username: username-for-registry.docker.innoactive.de
            registry_password: password-for-registry.docker.innoactive.de
            setup_database: true
            setup_wmc: true
            letsencrypt: true
            secret_key: not-secret-at-all-but-okay-for-tests
            hostname: my.hub.hostname.com
            admin_email: admin@innoactive.de

## Testing

For testing the role, different [molecule](https://testinfra.readthedocs.io) scenarios exist.

In either scenario, the following environment variables need to be set in your execution environment:

    DOCKER_REGISTRY_USERNAME

The username to use when authenticating against registry.docker.innoactive.de.

    DOCKER_REGISTRY_PASSWORD

The password to use when authenticating against registry.docker.innoactive.de.

### Docker

The first scenario applies the role to a local instance by using docker (and exposing the host's docker socket to the
docker containerp) so the Hub's containers are run as [siblings](https://stackoverflow.com/a/33003273/1142028) to the main
molecule container.

Testing the role with the docker driver bypasses some of the Hub's functionality like securing communication with
letsencrypt (which does not work if the host is not exposed to the internet).

To test the role using the scenario around the [docker driver](https://molecule.readthedocs.io/en/stable/configuration.html#docker)
simply run:

    molecule test

### Hetzner Cloud Server

To test the role in a more production-ready environment, molecule's hetzner cloud driver can be used to test the role
in a "Software-As-A-Service" (saas) scenario. The only thing required is an
[API token](https://docs.hetzner.cloud/#overview-getting-started) for Hetzner Cloud's API. Assuming this token is
available as `<api-token-for-hcloud>` simply run:

    HCLOUD_TOKEN=<api-token-for-hcloud> molecule test -s saas

## License

BSD

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
