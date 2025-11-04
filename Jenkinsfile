pipeline {
    agent any

    environment {
        IMAGE_NAME = "dakshish/multi-compose-flask"
        COMPOSE_FILE = "docker-compose.yml"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Checking out main branch..."
                git branch: 'main', url: 'https://github.com/Dakshish-Murthy/multi-compose-flask.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${env.IMAGE_NAME} ..."
                // Assumes Dockerfile is at repo root. If your Dockerfile is in app/, change '.' to '-f app/Dockerfile .'
                bat "docker build -t %IMAGE_NAME% ."
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo "Logging in to Docker Hub..."
                // Uses Jenkins credentials with id 'dockerhub'
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    // Use -p for Windows cmd login. If you prefer token, set password to token.
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo "Pushing image to Docker Hub: ${env.IMAGE_NAME} ..."
                bat "docker push %IMAGE_NAME%"
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo "Deploying with docker-compose..."
                 bat '''
                    dir
                    docker-compose down || exit 0
                    docker-compose up -d
                    '''
    }
}


        stage('Smoke Test (optional)') {
            steps {
                echo "Running quick smoke test (curl to http://localhost:5000)..."
                // Simple curl check using powershell's Invoke-WebRequest if curl not available
                // Try curl first; if curl not available, fall back to powershell Invoke-WebRequest
                bat """
                    powershell -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:5000' -TimeoutSec 10).StatusCode } catch { Write-Output 'SMOKE_TEST_FAILED'; exit 1 }"
                """
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Build or Deployment failed! Check console output for details.'
        }
        always {
            echo "Finished pipeline for ${env.IMAGE_NAME}"
        }
    }
}
