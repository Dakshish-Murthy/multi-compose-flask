pipeline {
    agent any

    environment {
        IMAGE_NAME = "dakshish/multi-compose-flask"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Dakshish-Murthy/multi-compose-flask.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                echo "Logging in to Docker Hub..."
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                echo "Pushing Docker image to Docker Hub..."
                bat 'docker push %IMAGE_NAME%'
            }
        }
    }

    post {
        success {
            echo '✅ Build and push completed successfully!'
        }
        failure {
            echo '❌ Build failed! Check console output for details.'
        }
    }
}
