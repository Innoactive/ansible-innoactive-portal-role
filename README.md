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

##### Device Mount / Drive

As an alternative to the Samba / CIFS share, we can also use a locally available device to store media files, as long
as the filesystem on this device is `ext4`. To make use of it, we need to configure as follows:

    media_volume_mount:
      device:
        path:

with:

    path:

An absolute path on the filesystem pointing to an `ext4`-formatted device.

##### Bind / Local Mount [DEPRECATED]

> [WARNING!]
> This option is deprecated and will be removed in the future

As an alternative to the Samba / CIFS share, we can also use an existing directory for the media files, as long
as the filesystem on this mountpoint is `ext4`. To make use of it, we need to configure as follows:

    media_volume_mount:
      local:
        path:

with:

    path:

An absolute path on the filesystem pointing to an existing directory.

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

### Telemetry Service / Analytics / Fluentd (Optional)

To enable the Hub's telemetry service / event database ("fluentd"), the following options need to be provided. This
service is entirely optional and if one of the values is not provided, it will not be set up.

    telemetry_shared_key:

A shared key used for authenticating trusted services running within the same stack. This shared key is e.g. used to log
event from another application server running on docker as well (like the django application) to the event collector.

    telemetry_salt:

Add some entropy to the hashing of sensitive user data within the events.

    telemetry_tls_privatekey:

Path to a valid TLS private key (on the local machine) that needs to be password protected. Used to decrypt incoming data
that has been encrypted using the TLS certificate.

    telemetry_tls_privatekey_passphrase:

Passphrase to unlock the TLS private key above.

    telemetry_tls_certificate:

TLS certificate that clients use to send their events in an encrypted and secure way.

    telemetry_tls_ca_certificate:

TLS certificate of the Certificate authority, i.e. the authority that signed the TLS certificate of both the event server
and the client certificate of any client sending data (used to validate the client certificate).

### Innoactive Hub Launcher

To enable the Innoactive Hub Launcher (a standalone application capable of retrieving content from the Hub) to access
data from the Hub, a suitable OAuth2 Client with the specified client credentials can be created if the following
parameters are provided (if none are provided, Launcher client will not be setup):

    launcher_oauth_client_id:

The OAuth2 Client ID that the Launcher uses.

    launcher_oauth_client_secret:

The OAuth2 Client Secret that the Launcher uses.

### Additional Hub Services

#### Innoactive Discovery Portal

    setup_discovery_portal: true

Whether or not to setup the discovery portal for this instance.

    portal_hostname: "portal.{{ hub_configuration.hostname  }}"

The hostname under which the discovery portal should be publicly availabe. This defaults to `portal.<hostname-of-hub-instance>`.

    portal_oauth_client_id:

Allows to explicitly define the oauth client id to be used by the portal to communicate with the Hub. If not defined,
an oauth client will automatically be retrieved.

    portal_oauth_client_secret:

Allows to explicitly define the oauth client secret to be used by the portal to communicate with the Hub. If not defined,
an oauth client will automatically be retrieved.

#### Innoactive Customization Service (for Discovery Portal)

    setup_customization_service: true

Whether or not to setup the customization service for this instance.

    customization_hostname: "customization.{{ hub_configuration.hostname  }}"

The hostname under which the customization service should be publicly availabe. This defaults to `customization.<hostname-of-hub-instance>`.

    customization_oauth_client_id:

Allows to explicitly define the oauth client id to be used by the portal to communicate with the Hub. If not defined,
an oauth client will automatically be retrieved.

    customization_oauth_client_secret:

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

## Tags

Since this role has quite a few steps and takes a while to execute, several tags exist that allow to dynamically disable
or enable parts of the role. See also [ansible docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_tags.html).

The available Tags are:

- *dependencies* (alias: *prerequisites*) Controls whether or not the (meta) dependencies of this role are being executed
  (docker and pip packages), more specific tags are available:

  - *docker* Controls whether the docker role dependency is being executed (might want to skip if Docker already installed)
  - *pip* Controls whether the pip role dependency is being executed

- *services* Controls whether or not all of the Hub's Services are being setup. More specifically, the individual services
  can be controlled with the following tags:

  - *base* Controls whether base services will be set up (Database, Message Queue, Mailserver)
  - *main* Controls whether main Hub services will be set up (Django application)
  - *ssl* Controls whether or not the Let's Encrypt service will be set up
  - *reverse_proxy* Controls whether or not the discovery portal service will be set up
  - *discovery_portal* Controls whether or not to start the reverse proxy service
  - *customization* Controls whether or not the customization service for the discovery portal will be set up
  - *telemetry* Controls whether or not the telemetry / analytics service will be set up

- *setup_tasks* Controls whether or not to run any setup tasks like database migrations, collection of static files, etc.

  - *user_groups* Controls whether or not to create an _Admins_ and _Users_ default group on the Hub instance. Both groups
    come with some predefined permissions to get started more easily. _Admins_ can do everything whereas _Users_ only can
    view and manage (upload) assets, applications, etc.
  - *superuser* Controls whether or not to create a superuser account
  - *launcher* Controls whether or not to create an oauth2 client for the Innoactive Hub Launcher

- *requires_database* Allows to skip all tasks that require a running database (e.g. because the database should not be
  filled with data as a previous dump should be imported)

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
