# Role Name

A brief description of the role goes here.

## Requirements

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the
role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

## Role Variables

A description of the settable variables for this role should go here, including any variables that are in
defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables
that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

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

    setup_database: true

Whether to run database migrations and setup the database.

    setup_wmc: true

Whether to make the static frontend assets available on the Hub instance (styles, images, scripts). I.e. setup the frontend.

    sentry_dsn:

DSN for [Sentry](https://sentry.io/welcome/) to automatically track runtime errors.

    google_analytics_tracking_id:

Tracking ID of a Google Analytics Property to monitor usage of the Hub.

### Secured Communication

    letsencrypt: true

Whether or not to use [Let's Encrypt](https://letsencrypt.org/) to issue SSL / TLS certificates. Set this to false if
you intend to use custom certificates or no certificates at all.

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

- [burnedikt.pip](https://github.com/burnedikt/ansible-role-pip)

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
