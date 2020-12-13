import groovy.json.JsonOutput
import groovy.json.JsonSlurper

pipeline {
    agent {
        label 'node003'
    }

    environment {
        JAVA_HOME = "/usr/lib/jvm/jdk1.8.0_251"
        MAVEN_CONFIG = "/root/.m2/"
        M2_HOME = "/usr/lib/maven/apache-maven-3.6.3"
        gitrepourl = 'git@github.com:wiz4host/infra-maven-project.git'
        gitcredid = 'github-wiz4host-SSHKEY'
        nexusbaseurl = 'http://10.0.0.103:8081/'
        release_ver = '1.0'
        ENVIRONMENT = env.BRANCH_NAME
        TFE_BASE_URL = "https://terraform.dev.sys.mx.us.dev.corp/api/v2/organizations/"
        WORKSPACE_NAME="Test_TFE1"
        ORGANIZATION_NAME="POC02"

    }
    stages {

        stage("ws clean") {
            steps{
                cleanWs()
            }
        }

        stage("git pull") {
            steps{
                checkout([$class: 'GitSCM',
                          branches: scm.branches,
                          extensions: scm.extensions + [[$class: 'CleanCheckout']],
                          submoduleCfg: [],
                          userRemoteConfigs: [[credentialsId: gitcredid, url: gitrepourl]]
                ])
            }

        }


        stage("TFE Create WS"){
            steps{
                withCredentials([
                        string(credentialsId: 'TFE_BEARER_TOKEN', variable: 'tfebearertoken')
                ]){
                    sh """
                        curl -k --location --request POST "${TFE_BASE_URL}/${ORGANIZATION_NAME}/workspaces' \
                           --header 'Content-Type: application/vnd.api+json' \
                           --header 'Authorization: Bearer ${tfebearertoken}' \
                           --data '{
                                "data": {
                                     "attributes": {
                                          "name": "${WORKSPACE_NAME}",
                                      },
                                     "type": "workspaces"
                                }
                           }' > ${env.BUILD_NUMBER}-cw-response.json
                    """

                    def response = readFile(env.BUILD_NUMBER+'-cw-response.json').trim()
                    def data = new JsonSlurper().parseText(response)
                    WORKSPACE_ID = data.data.id
                    println ("Workspace Id: ${WORKSPACE_ID}")
                    sh "echo ${WORKSPACE_ID} | tee ./workspace-BLD${BUILD_NUMBER}.id"
                }
            }

        }

        stage("TFE Upload"){
            environment{
                tftarcontentdir =  "./content"
            }
            steps{
                withCredentials([
                        string(credentialsId: 'TFE_BEARER_TOKEN', variable: 'tfebearertoken')
                ]){
                   steps{
                       sh "./terraform-enterprise-push.sh ${tftarcontentdir} ${ORGANIZATION_NAME}/${WORKSPACE_NAME} ${BUILD_NUMBER} ${tfebearertoken}"
                   }
                }

            }

        }

        stage("TFE Plan"){
            echo "Upload TF code to WorkSpace"

        }

        stage("TFE Sentinel"){
            echo "Scan TF code with Sentinel"

        }

        stage("TFE Delete WS"){
            echo "Delete TFE Workspace"

        }

        stage("mvn prepare") {
            steps{
                withCredentials([file(credentialsId: 'maven-encrypt-master-key-file', variable: 'mvncryptmasterkeyfile')]) {
                    sh "cp \$mvncryptmasterkeyfile \${MAVEN_CONFIG}/"
                }
            }
        }

        stage("mvn zip") {
            steps {
                script {
                    switch (${ENVIRONMENT }) {
                        case "development": sh "mvn -s settings-nexus.xml -Dnexusbaseurl=\$nexusbaseurl -Dversion=\${release_ver}-SNAPSHOT  clean package"; break
                        case "production": sh "mvn -s settings-nexus.xml -Dnexusbaseurl=\$nexusbaseurl -Dversion=\${release_ver}  clean package"; break
                        default: echo "Nothing to do"; break
                    }
                }
            }
        }

        stage("mvn upload") {
            steps {
                script {
                    switch (${ENVIRONMENT }) {
                        case "development": sh "mvn -s settings-nexus.xml -Dnexusbaseurl=\$nexusbaseurl -Dversion=\${release_ver}-SNAPSHOT  deploy"; break
                        case "production": sh "mvn -s settings-nexus.xml -Dnexusbaseurl=\$nexusbaseurl -Dversion=\${release_ver}  deploy"; break
                        default: echo "Nothing to do"; break
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'This will always run'
            sh "echo ${ENVIRONMENT}"
        }
        success {
            echo 'This will run only if successful'
            //mail to:"me@example.com", subject:"SUCCESS: ${currentBuild.fullDisplayName}", body: "Yay, we passed."
        }
        failure {
            echo 'This will run only if failed'
            //mail to:"me@example.com", subject:"FAILURE: ${currentBuild.fullDisplayName}", body: "Boo, we failed."
        }
        unstable {
            echo 'This will run only if the run was marked as unstable'
            //mail to:"me@example.com", subject:"UNSTABLE: ${currentBuild.fullDisplayName}", body: "Huh, we're unstable."
        }
        changed {
            echo 'This will run only if the state of the Pipeline has changed'
            echo 'For example, if the Pipeline was previously failing but is now successful'
            //mail to:"me@example.com", subject:"CHANGED: ${currentBuild.fullDisplayName}", body: "Wow, our status changed!"
        }
    }
}
