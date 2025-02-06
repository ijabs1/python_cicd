pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_REPO = 'asaoluolalekan1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    python3 -m pip install --user -r requirements.txt
                    python3 -m pip install --user pytest
                '''
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m pytest test/'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Replace invalid characters in branch name
                    def sanitizedBranch = env.BRANCH_NAME.replaceAll('/', '-').toLowerCase()
                    def imageTag = "${sanitizedBranch}-${env.BUILD_NUMBER}"

                    sh """
                        docker build -t ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag} .
                    """
                }
            }
        }

        stage('Push to Docker Registry') {
            steps {
                script {
                    def sanitizedBranch = env.BRANCH_NAME.replaceAll('/', '-').toLowerCase()
                    def imageTag = "${sanitizedBranch}-${env.BUILD_NUMBER}"

                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo "$DOCKER_PASS" | docker login ${DOCKER_REGISTRY} -u "$DOCKER_USER" --password-stdin
                        '''
                    }

                    sh """
                        docker push ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag}
                    """

                    sh 'docker logout ${DOCKER_REGISTRY}'
                }
            }
        }
    }

    post {
        always {
            cleanWs()
            script {
                def sanitizedBranch = env.BRANCH_NAME.replaceAll('/', '-').toLowerCase()
                def imageTag = "${sanitizedBranch}-${env.BUILD_NUMBER}"

                sh """
                    docker rmi ${DOCKER_REGISTRY}/${DOCKER_REPO}:${imageTag} || true
                    docker system prune -f || true
                """
            }
        }
    }
}
