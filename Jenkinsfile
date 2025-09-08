pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Project') {
            steps {
                sh ''' 
                     
                    cd $WORKSPACE 
                    docker compose up -d --build --force-recreate
                '''
            }
        }
    }
}
