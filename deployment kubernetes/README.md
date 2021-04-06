# Jenkins Pipeline to Deoploy Application into kubernetes cluster using AWS

## Prerequisites
S
AWS account


## Create a key pair
### To create your key pair:
- Amazon EC2 console sign in.
- Navigate to  NETWORK & SECURITY, choose Key Pairs.
- Select Create key pair>>> enter a descriptive name for the key pair. 

Amazon EC2 associates the public key with the name as specified above in the key name. 


For private key saving can be done:

1. In format that can be used with OpenSSH, choose pem.

2. In format that can be used with PuTTY, choose ppk.

key pair name is the base file name and the extension is determined by the format choosen. 

***$ chmod 400 key_pair_name.pem***

Permissions are set to  connect the instance using this key pair.
 
## Create a Security Group(SG)
- SG acts as a firewall that controls the traffic and allows to reach one or more EC2 instances. 
- When instance is lanched one or more security groups can be assigned.
- Rules can be added to each SG for controlling  the traffic to reach the instances  

Here security group and add the following rules :

1. Allow inbound HTTP access from anywhere. 
2. Allow inbound SSH traffic from your computer’s public IP address enables connection  to the instance created.

***Note:*** For creating  and configuring the security group in general need to consider who will access the instance, 

Here used the public IP address of my computer. 
To find the IP address, used the checkip service from AWS3 or 
alternatively can search "what is my IP address" in any Internet search engine. 

In Security group name enter WebServerSG or any preferred name of your choice and provide a description.

 default VPC is used 

- On the Inbound tab, add the rules as follows:

   Click Add Rule >>> choose SSH from the Type list. 
Under Source>>>select Custom and in the text box enter public IP address range 

   Click Add Rule>>>choose HTTP from the Type list.

   Click Add Rule>>>choose Custom TCP Rule from the Type list.Port Range enter 8080.
>>>Click Create.

## Launch an Amazon EC2 instance
- AWS Management Console Sign in

- Open the Amazon EC2 console choosing EC2 under Compute.

- Amazon EC2 dashboard >>> choose Launch Instance >>>Ubuntu
>>> t2.micro instance (default) for worker  and t2.medium for master  >>> Review and Launch.

In the Configure Security Group page:
Selected an existing security group>>> WebServerSG security group created >>> Review and Launch.

In the Select an existing key pair or create a new key pair dialog box:

Selected Choose an existing key pair>>>
Select the key pair you created in the [Create a key pair using Amazon EC2]

In the left-hand navigation bar, choose Instances to see the status of instance.
Initially, the status of instance is pending.
After the status changes to running,the instance is ready for use.

## Install and Configure Jenkins on EC2 Instance 
### Connect the  Linux instance: 
- After launching instance: can connect to it and use it the way  would need in  local machine.

- Before connecting  to  instance >>> get the public DNS name of the instance using the Amazon EC2 console>>>Select the instance and locate Public DNS.

### Using PuTTY for connectting the  instance
From the Start menu>>> All Programs > PuTTY > PuTTY.

- Category pane >>> Session >>> Host Name, enter ec2-user@public_dns_name >>> Port is 22.


-  Category pane >>> Connection >>> SSH >>> Auth >>> Click Browse.

- .ppk file (generated for your key pair)  >>> Open:  start the PuTTY session


## Installing Jenkins

### JCasC
-Jenkins Configration as code 
- provides the ability to define the whole config as simple , human friendly , plain text 
- The ability to reproduce or restore a full envi within minutes based on automation manged as code :config as code 
- yaml synatx 
- without a manual step config can validate and applied to jenkins controller in fully reproducible way 
1. config all jenkins initial setup 
2. supports most plugins without extra development effort

Steps to install jenkins

**Case:1**

1. open ubuntu terminal

2. check whether docker is install or not.if not install docker 

3. After installation check the version using 
**docker --version**

4. now we have to pull the jenkins from the docker hub using following command
**docker pull jenkins**

5. once image pulled and check by using **docker images**

6. once image is created we have to run the container using
**docker run -d --name container_name -p 8080:8080 -p 50000:50000 -v/var/jenkins_home jenkins**

this is locally running 
### Configure Jenkins 
- Connect to http://<your_server_public_DNS>:8080 check in any browser. 
- Now it will be able to access Jenkins through its management interface:
As prompted, enter the password found in /var/lib/jenkins/secrets/initialAdminPassword.

Use the following command to display this password: 

7. after running the container we get the password.if we did not get type **docker logs container_id**

8. To unlock jenkins use the step 7 process

9. After unlocking install all dependencies.

>>> Manage Jenkins>>> Manage Plugins.

>>> Available tab>>> Amazon EC2 plugin >>kubernetes >>>kubernetes continuous deploy
>>> click Install without restart.

After installation is done >>> Back to Dashboard.

>>> Configure a cloud >>>  Add a new cloud >>> Amazon EC2. 

### Installations 

1. **On each server, install Docker**

curl -fsSL https://download.docker.com/linux/ubu...​ | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu​ $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install -y docker-ce

2.  **On each server, install kubernetes**
(Installation guide: https://kubernetes.io/docs/setup/prod...​)
curl -s https://packages.cloud.google.com/apt...​ | sudo apt-key add -
cat &lt&lt EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/​ kubernetes-xenial main
EOF
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

3.  **On each server, enable the use of iptables**
echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

4. **On the Master server only, initialize the cluster**
sudo kubeadm init --pod-network-cidr=10.244.0.0/16


5. **On the Master server only, set up the kubernetes configuration file for general usage**
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

6. **On the Master server only, apply a common networking plugin.**
 In this case, Flannel
kubectl apply -f https://raw.githubusercontent.com/cor...​

7. On the Worker servers only, join them to the cluster using the command you copied earlier. 
kubeadm join 172.31.37.80:6443 --token ... --discovery-token-ca-cert-has

## Pipeline 

In order Jenkins to deploy to Kubernetes, Jenkins needs credentials

credentials>>> cloud configs >>>add new cloud >>>Kuberenetes cloud details >>>config file added in Jenkins>>>test connection 


This file is usually used by kubectl and found in .kube/config. 
It allows Jenkins to apply yaml configuration to a Kubernetes instance.
>>> add jenkins url >>>jenkins tunnel - add the slave listening port url 

>>>pod template >>>pod template details >> ADD name >>> ADD label>>> ADD container and command to run >>>

Label mentioned here in this setting it is used in pipeline script 

>>>credentials >>>system >>>global credentials >>> select kind : kubernetes configuration >>> kube config : select enter directly >>> add the config file text in this field

 >>>kubectl get all command to check 

>>>jenkins dash board >>> create new item  : select  pipeline as job >>> add the pipeline script scm >>> git as scm here choosen >>> add the branch to build >>> save 

triggerring this job and check using command 
***kubectl  get all*** :can see new slave pod which will execute the stages in the pipeline. 





