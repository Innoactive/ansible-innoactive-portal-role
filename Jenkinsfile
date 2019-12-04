pipeline {
    agent {
        label 'ansible-and-docker'
    }

    environment {
        SANITIZED_BUILD_TAG = "${GIT_COMMIT}" + "${BUILD_NUMBER}"
    }

    stages {
        stage('Setup') {
            steps {
                sh "sudo apt-get install -y python3-distutils"
                sh "pipenv install"
            }
        }
        stage('Test') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'innoactive-docker-registry', passwordVariable: 'REGISTRY_PASSWORD', usernameVariable: 'REGISTRY_USERNAME')]) {
                    withEnv(["DOCKER_REGISTRY_USERNAME=${REGISTRY_USERNAME}", "DOCKER_REGISTRY_PASSWORD=${REGISTRY_PASSWORD}", "INSTANCE_NAME_SUFFIX=-${SANITIZED_BUILD_TAG}", "PATH+VENV=${sh(script: 'pipenv --venv', returnStdout: true).trim()}/bin"]) {
                        ansiColor('xterm') {
                            sh "molecule test"
                        }

                        withCredentials([string(credentialsId: 'molecule-hcloud-api-token', variable: 'hcloud_api_token')]) {
                            withEnv(["HCLOUD_TOKEN=$hcloud_api_token"]) {
                                ansiColor('xterm') {
                                    sh "molecule test -s saas"
                                    sh "molecule test -s with_cifs"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
