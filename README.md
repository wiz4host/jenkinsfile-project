# jenkinsfile-project

withCredentials([sshUserPrivateKey(credentialsId: "yourkeyid", keyFileVariable: 'keyfile')]) {
       stage('scp-f/b') {
        sh "scp -i ${keyfile} do sth here"
       }
   }


withCredentials([file(credentialsId: PRIVATE_KEY, variable: 'my_private_key'),
                 file(credentialsId: PUBLIC_KEY, variable: 'my_public_key')]) {
        writeFile file: 'key/private.pem', text: readFile(my_private_key)
        writeFile file: 'key/public.pem', text: readFile(my_public_key)
    }

kubectl create secret tls test-tls --key="tls.key" --cert="tls.crt"
