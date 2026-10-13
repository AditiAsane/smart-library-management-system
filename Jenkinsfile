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

                    BACKUP="${APP_CONTAINER}-previous"

                    echo "Starting deployment..."

                    # Remove any stale backup
                    docker rm -f "$BACKUP" 2>/dev/null || true

                    # Stop the current app to release port 5000
                    if docker container inspect "$APP_CONTAINER" >/dev/null 2>&1; then
                        docker stop "$APP_CONTAINER"
                        docker rename "$APP_CONTAINER" "$BACKUP"
                    fi

                    # Start the new version
                    if ! docker run -d \
                        --name "$APP_CONTAINER" \
                        --restart unless-stopped \
                        -p "${APP_PORT}:5000" \
                        "$APP_IMAGE"; then

                        echo "Container startup failed. Rolling back..."
                        docker rm -f "$APP_CONTAINER" 2>/dev/null || true

                        if docker container inspect "$BACKUP" >/dev/null 2>&1; then
                            docker rename "$BACKUP" "$APP_CONTAINER"
                            docker start "$APP_CONTAINER"
                        fi

                        exit 1
                    fi

                    # Check application health
                    echo "Checking application health..."
                    HEALTHY=0

                    for i in $(seq 1 15); do
                        if curl -fsS "http://127.0.0.1:${APP_PORT}/" >/dev/null; then
                            HEALTHY=1
                            break
                        fi
                        sleep 2
                    done

                    # Roll back if the health check fails
                    if [ "$HEALTHY" -ne 1 ]; then
                        echo "Health check failed. Rolling back..."
                        docker rm -f "$APP_CONTAINER" 2>/dev/null || true

                        if docker container inspect "$BACKUP" >/dev/null 2>&1; then
                            docker rename "$BACKUP" "$APP_CONTAINER"
                            docker start "$APP_CONTAINER"
                        fi

                        exit 1
                    fi

                    # Keep the new version only after a successful health check
                    docker rm -f "$BACKUP" 2>/dev/null || true

                    echo "Deployment completed successfully!"
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
