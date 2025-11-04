pipeline {
    agent any

    environment {
        IMAGE_NAME = "dakshishmurthy/multi-compose-flask"  // ✅ your Docker Hub repo
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Cloning repository..."
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
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
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

        stage('Deploy with Docker Compose') {
            steps {
                echo "Deploying containers using docker-compose..."
                // Clean up old containers and networks if they exist
                bat 'docker-compose down || exit 0'
                // Rebuild and start fresh containers
                bat 'docker-compose up -d --build'
            }
        }

        // 🔇 Smoke Test disabled (optional)
        // stage('Smoke Test (optional)') {
        //     steps {
        //         echo 'Running quick smoke test...'
        //         bat """
        //         powershell -Command "try { (Invoke-WebRequest -UseBasicParsing -Uri 'http://localhost:5000' -TimeoutSec 10).StatusCode } catch { Write-Output 'SMOKE_TEST_FAILED'; exit 1 }"
        //         """
        //     }
        // }
    }

    post {
        success {
            echo '✅ Build, push, and deployment completed successfully!'
        }
        failure {
            echo '❌ Build or deployment failed! Please check console output.'
        }
    }
}
