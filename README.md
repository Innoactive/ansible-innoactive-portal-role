# Ansible Innoactive Portal Role

[![Build Status](https://dev.azure.com/Innoactive/Open-Source/_apis/build/status/Innoactive.ansible-innoactive-portal-role?branchName=develop)](https://dev.azure.com/Innoactive/Open-Source/_build/latest?definitionId=29&branchName=develop)

This role sets up a host to run the Innoactive Portal - XR platform.

## Requirements

Since the deployment uses [json_query](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html#json-query-filter)
to extract important values from json data structures, the respective pip package [jmespath](http://jmespath.org/) needs
to be installed locally via pip.

Also, the Innoactive Portal's images are distributed via Innoactive's private Docker registry so in order to access and deploy
them, credentials to access the docker registry at `registry.docker.innoactive.de` are required.

Since the Innoactive Portal consists of a number of services each of which is bundled as a docker container, this role requires the ansible host to have [docker](https://www.docker.com/) installed (API level >= 1.20) and ready to use. To ensure this, you can e.g. use the excellent ansible role [geerlingguy.docker](https://galaxy.ansible.com/geerlingguy/docker).

Additionally, ansible's [docker module](https://docs.ansible.com/ansible/latest/modules/docker_container_module.html) requires the docker pip module to be installed in order for Python to be able to communicate with the running docker service. Installing this package can e.g. either be done via the native ansible [pip module(https://docs.ansible.com/ansible/latest/modules/pip_module.html)] or via a dedicated role like [geerlingguy.pip](https://galaxy.ansible.com/geerlingguy/pip).

## Installation

To install this role locally, simply run `ansible-galaxy install git+git@github.com:Innoactive/ansible-innoactive-hub-role.git`.

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

### Docker Registry

    registry_hostname: registry.docker.innoactive.de

The registry from which to pull images of the Portal's containers.

    registry_username:

The username to use to authenticate against the specified docker registry.

    registry_password:

The password to use to authenticate against the specified docker registry.

### Innoactive Portal

    portal_hostname:

**Mandatory** hostname under which the Portal will be available (this needs to be publicly reachable).

    portal_alias_hostnames: []

Alternative or legacy hostnames array. Users accessing it will be redirected to portal_hostname.

    admin_hostname:

**Mandatory** hostname under which the portal control panel will be available.

    admin_alias_hostnames: []

Alternative or legacy hostnames array. Users accessing it will be redirected to admin_hostname.

    customization_hostname:

**Mandatory** hostname under shich the customization service will be available.

    customization_alias_hostnames: []

Alternative or legacy hostnames array. Users accessing it will be redirected to customization_hostname.

    secret_key:

A user-defined, secret key used for salting hashes within the Portal's backend service. Never expose this to anyone!

    from_email:

E-Mail address from which to send transactional e-mails (e.g. onboarding) to users. If not provided, uses `admin_email`, see below.

    admin_email:

E-Mail address of the main admin user, used to notify upon errors, expired certificates, etc.

    admin_password:

Password of the main admin user to login to the Portal backend and manage other users or content.

    create_admin_user: true

Whether to ensure the creation of an admin user on the Portal backend, may be skipped if users are setup manually.

    setup_database: true

Whether to run database migrations and setup the database.

    setup_control_panel: true

Whether to make the static frontend assets available on the Portal backend (styles, images, scripts). I.e. setup the control panel (f.k.a
Web Management Console or WMC). Legacy Option: `setup_wmc: true`

    sentry_dsn:

DSN for [Sentry](https://sentry.io/welcome/) to automatically track runtime errors.

    google_analytics_tracking_id:

Tracking ID of a Google Analytics Property to monitor usage of the Portal Backend.

    extra_environment_variables: {}

Optional mapping of additional environment variables to be passed on to the Portal Backend (e.g. to unlock hidden features).

    traefik_dashboard:

Optional boolean allowing to enable the [traefiks dashboard](https://docs.traefik.io/operations/dashboard/) and therefore see the current routing configuration.

    traefik_extra_config_path:

Optional string to configure a folder that gets mapped in the traefik container. This is useful to provide additional configuration files for traefik such as a usersfile for [basic authentication](https://doc.traefik.io/traefik/middlewares/basicauth/). Defaults to `/etc/hub/traefik`

    traefik_docker_extra_config_path:

Optional string to configure a folder within the traefik container where the extra config folder is mapped to. Defaults to `/custom_config`

    traefik_enable_tls

Optional bool to enable / disable tsl. Defaults to `true`

    traefik_certificate_resolver

Optional string to set a custom certificate resolver. Useful when using self signed certificates instaed of lets-encrypt. Defaults to `lets-encrypt`

    traefik_extra_env_vars

Optional key-value pair to set additional environment variables on the traefik container. Defaults to `{}`

    traefik_extra_labels

Optional key-value pair to set additional labels on the traefik container.  Defaults to `{}`

#### Media Files

The Portal Backend's files (user uploads like applications, assets, ...) are stored within a dedicated docker volume. To ensure
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

It is possible to deploy different versions of Innoactive Portal's services by specifying the following variables.
Available versions for the docker container images can be found in our registry at `registry.docker.innoactive.de`.

    portal_image_version: latest

The version of Innoactive Portal's frontend container.

    portal_backend_image_version: latest

The version of Innoactive Portal's backend container. Legacy parameter: `hub_image_version: latest`

    reverse_proxy_image_version: 2.2

The version of the reverse proxy ([traefik]) image to be used.

### Secured Communication

    letsencrypt: true

Whether or not to use [Let's Encrypt](https://letsencrypt.org/) to issue SSL / TLS certificates. Set this to false if
you intend to use custom certificates or no certificates at all.

    letsencrypt_test: false

When using [Let's Encrypt](https://letsencrypt.org/) to issue SSL / TLS certificates this flag (defaults to false) can be
used to issue certificates by Let's Encrypt's [staging environment](https://letsencrypt.org/docs/staging-environment/)
instead of the production environment.

### CloudXR Management Service

    cloudxr_enabled:

**Mandatory** If false, the container is not deployed. Defaults to `false`

    cloudxr_default_region:

**Mandatory** Default region if ip lookup did not work

    cloudxr_instance:

The instance (customer). Defaults to `instance_name` variable.

    cloudxr_max_cloud_instances:

**Mandatory** The maximum started instance across all regions.

    cloudxr_machine_max_keep_alive_age:

**Mandatory** The keepalive age time untill machine is destroyed. Format: hh:MM:ss (04:00:00)

    cloudxr_management_sentry_dsn:

The sentry DSN

    cloudxr_ip_stack_api_token:

**Mandatory** The IP address lookup is required to select the closest cloudXR region. The token must be obtained on [this](https://ipstack.com/) website

    cloudxr_azure_enabled:

**Mandatory if azure** enable azure integration. This option is mutually exclusive with `cloudxr_aws_enabled`

    cloudxr_azure_client_id:

**Mandatory if azure** azure clientID to control the scale set

    cloudxr_azure_secret:

**Mandatory if azure** azure client secret to control the scale set

    cloudxr_azure_subscription:

**Mandatory if azure** azure subscription where the scaleset is deployed

    cloudxr_azure_tenant_id:

**Mandatory if azure** azure tenant where the scaleset is deployed

    cloudxr_aws_enabled:

**Mandatory if aws** enable AWS integration. This option is mutually exclusive with `cloudxr_azure_enabled`

    cloudxr_aws_access_key_id:

**Mandatory if aws** access key id to the aws scaling group

    cloudxr_aws_secret_access_key:

**Mandatory if aws** access key secret to the aws scaling group

    cloudxr_aws_regions:

**Mandatory if aws** all regions where scaling groups are deployed (as they cannot be detected automatically)

### Session Management Service

    session_management_image_version:

The version of the session mangement contianer. This defaults to `latest`

    session_management_sentry_dsn:

The sentry dsn url

    session_management_environment:

The environment `Production`, `Staging`, `Developtment`. This defaults to `Production`

    session_management_cors_origin:

If custom CORS origin(s) are required it can be set here separated by `,` (comma)

    session_management_oauth_client_id:

**Mandatory** the OAuth clientID

    session_management_oauth_client_secret:

**Mandatory** the OAuth client secret

    session_management_log_level:

The log level. This defaults to `Warning`

### Innoactive Portal Desktop Client (f.k.a Hub Launcher)

To enable the Innoactive Portal Desktop Client (a standalone application capable of retrieving content from the Portal) to access
data from the Portal, a suitable OAuth2 Client with the specified client credentials can be created if the following
parameters are provided (if none are provided, Desktop Client client will not be setup):

    desktop_client_oauth2_client_id:

The OAuth2 Client ID that the Launcher uses. (Legacy option: `launcher_oauth_client_id`)

    desktop_client_oauth2_client_secret:

The OAuth2 Client Secret that the Launcher uses. (Legacy option: `launcher_oauth_client_secret`)

### Additional Portal Services

#### Innoactive Portal Frontend

    setup_discovery_portal: true

Whether or not to setup the Portal frontend for this instance.

    portal_hostname: "portal.{{ admin_configuration.primay_hostname  }}"

The hostname under which the Portal frontend should be publicly availabe. This defaults to `portal.<hostname-of-portal-instance>`.

    portal_oauth_client_id:

Allows to explicitly define the oauth client id to be used by the portal to communicate with the Portal backend. If not defined,
an oauth client will automatically be retrieved.

    portal_sentry_dsn:

DSN for [Sentry](https://sentry.io/welcome/) to automatically track runtime errors within the Portal.

    portal_extra_environment_variables: {}

Optional mapping of additional environment variables to be passed on to the Portal (e.g. to unlock hidden features).

#### Innoactive Customization Service (for Discovery Portal)

    setup_customization_service: true

Whether or not to setup the customization service for this instance.

    customization_hostname: "{{ customization_configuration.hostname  }}"

The hostname under which the customization service should be publicly availabe. This defaults to `customization.<hostname-of-portal-instance>`.

    customization_oauth_client_id:

Allows to explicitly define the oauth client id to be used by the portal to communicate with the Portal backend. If not defined,
an oauth client will automatically be retrieved.

    customization_oauth_client_secret:

Allows to explicitly define the oauth client secret to be used by the portal to communicate with the Portal backend. If not defined,
an oauth client will automatically be retrieved.

    customization_extra_environment_variables: {}

Optional mapping of additional environment variables to be passed on to the Portal Backend (e.g. to unlock hidden features).

### Mail Setup

In order to send mails, SMTP needs to be set up

    smtp_host:

The host adress of the SMTP server.

    smtp_port:

The port used by the SMTP server.

    smtp_user:

The SMTP user to authenticate with.

    smtp_password:

The password corresponding to the given SMTP user.

    smtp_use_tls: no

Whether or not (boolean) the SMTP server requires the use of TLS. Mutually exclusive with `use_ssl`.

    smtp_use_ssl: no

Whether or not (boolean) the SMTP server requires the use of SSL. Mutually exclusive with `use_tls`.

## Dependencies

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set
for other roles, or variables that are used from other roles.

- [geerlingguy.pip](https://github.com/geerlingguy/ansible-role-pip)

If the server to which to apply the Innoactive Portal role to does not come with docker pre-installed, it is helpful to also
use:

- [geerlingguy.docker](https://github.com/geerlingguy/ansible-role-docker)

## Tags

Since this role has quite a few steps and takes a while to execute, several tags exist that allow to dynamically disable
or enable parts of the role. See also [ansible docs](https://docs.ansible.com/ansible/latest/user_guide/playbooks_tags.html).

The available Tags are:

- _dependencies_ (alias: _prerequisites_) Controls whether or not the (meta) dependencies of this role are being executed
  (docker and pip packages), more specific tags are available:

  - _docker_ Controls whether the docker role dependency is being executed (might want to skip if Docker already installed)
  - _pip_ Controls whether the pip role dependency is being executed

- _services_ Controls whether or not all of the Portal's Services are being setup. More specifically, the individual services
  can be controlled with the following tags:

  - _base_ Controls whether base services will be set up (Database, Message Queue, Mailserver)
  - _main_ Controls whether main Portal services will be set up (Django application / Backend)
  - _ssl_ Controls whether or not the Let's Encrypt service will be set up
  - _reverse_proxy_ Controls whether or not the discovery portal service will be set up
  - _discovery_portal_ Controls whether or not to start the reverse proxy service
  - _customization_ Controls whether or not the customization service for the discovery portal will be set up

- _setup_tasks_ Controls whether or not to run any setup tasks like database migrations, collection of static files, etc.

  - _user_groups_ Controls whether or not to create an _Admins_ and _Users_ default group on the Portal instance. Both groups
    come with some predefined permissions to get started more easily. _Admins_ can do everything whereas _Users_ only can
    view and manage (upload) assets, applications, etc.
  - _superuser_ Controls whether or not to create a superuser account
  - _launcher_ Controls whether or not to create an oauth2 client for the Innoactive Portal Desktop Client

- _requires_database_ Allows to skip all tasks that require a running database (e.g. because the database should not be
  filled with data as a previous dump should be imported)

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for
users too:

    - hosts: servers
      roles:
        - role: geerlingguy.docker
          become: true
        - role: innoactive.portal
          vars:
            # main configuration parameters
            registry_username: username-for-registry.docker.innoactive.de
            registry_password: password-for-registry.docker.innoactive.de
            setup_database: true
            setup_control_panel: true
            letsencrypt: true
            secret_key: not-secret-at-all-but-okay-for-tests
            admin_email: admin@innoactive.de
            portal_hostname: portal.my.hostname.com
            admin_hostname: admin.portal.my.hostname.com
            customization_hostname: customization.portal.my.hostname.com

## Upgrading from 1.x to 2.x

With version 2 of this role, we've introduced a breaking change by ensuring that data created by the Portal is stored in
named docker volumes rather than anonymous ones (which can easily get lost). To ease the transition from Portal instances
that were deployed with Version 1.x of this role, we've created a simple ansible playbook that helps by migrating all
data previously stored in anonymous volumes to the new set of named volumes. After running this playbook on the host in
question, Version 2.x of this role can simply be applied without the fear of losing data. See
[here](migration/anonymous_to_named_volumes.yml) for the migration playbook.

## Testing

For testing the role, different [molecule](https://testinfra.readthedocs.io) scenarios exist.

In either scenario, the following environment variables need to be set in your execution environment:

    DOCKER_REGISTRY_USERNAME

The username to use when authenticating against registry.docker.innoactive.de.

    DOCKER_REGISTRY_PASSWORD

The password to use when authenticating against registry.docker.innoactive.de.

### Docker

The first scenario applies the role to a local instance by using docker (and exposing the host's docker socket to the
docker containerp) so the Portal's containers are run as [siblings](https://stackoverflow.com/a/33003273/1142028) to the main
molecule container.

Testing the role with the docker driver bypasses some of the Portal's functionality like securing communication with
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

[Apache 2.0](LICENSE)

## Author Information

An optional section for the role authors to include contact information, or a website (HTML is not allowed).

[traefik]: https://hub.docker.com/_/traefik
