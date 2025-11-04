pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'dakshish/multi-compose-flask'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Dakshish-Murthy/multi-compose-flask.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t %DOCKER_IMAGE% -f app/Dockerfile .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASS')]) {
                    bat 'docker login -u %DOCKER_HUB_USER% -p %DOCKER_HUB_PASS%'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                bat 'docker push %DOCKER_IMAGE%'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                echo 'Deploying application with Docker Compose...'
                // Stop any previous containers (if running)
                bat 'docker-compose down || exit 0'
                // Start fresh containers
                bat 'docker-compose up -d'
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD pipeline completed successfully!'
        }
        failure {
            echo '❌ Build or Deployment failed!'
        }
    }
}
