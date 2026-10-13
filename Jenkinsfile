pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        APP_IMAGE = 'smart-library:ci'
        APP_CONTAINER = 'smart-library'
        APP_PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv .ci-venv
                    .ci-venv/bin/pip install --upgrade pip
                    .ci-venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '.ci-venv/bin/python -m pytest -q'
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t "$APP_IMAGE" .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -eu

                    docker rm -f "${APP_CONTAINER}-previous" 2>/dev/null || true

                    if docker container inspect "$APP_CONTAINER" >/dev/null 2>&1; then
                        docker rename "$APP_CONTAINER" "${APP_CONTAINER}-previous"
                    fi

                    if ! docker run -d \
                        --name "$APP_CONTAINER" \
                        --restart unless-stopped \
                        -p "${APP_PORT}:5000" \
                        "$APP_IMAGE"; then
                        docker rm -f "$APP_CONTAINER" 2>/dev/null || true

                        if docker container inspect "${APP_CONTAINER}-previous" >/dev/null 2>&1; then
                            docker rename "${APP_CONTAINER}-previous" "$APP_CONTAINER"
                            docker start "$APP_CONTAINER"
                        fi

                        exit 1
                    fi

                    sleep 5

                    if ! curl --fail --silent \
                        http://127.0.0.1:${APP_PORT}/api/health; then
                        docker rm -f "$APP_CONTAINER" || true

                        if docker container inspect "${APP_CONTAINER}-previous" >/dev/null 2>&1; then
                            docker rename "${APP_CONTAINER}-previous" "$APP_CONTAINER"
                            docker start "$APP_CONTAINER"
                        fi

                        exit 1
                    fi

                    docker rm -f "${APP_CONTAINER}-previous" 2>/dev/null || true
                '''
            }
        }
    }

    post {
        always {
            sh 'rm -rf .ci-venv'
        }
        success {
            echo 'CI/CD completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs before retrying.'
        }
    }
}
