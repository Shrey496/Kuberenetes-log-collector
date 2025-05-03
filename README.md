# Kubernetes log collector

# Description: 
This project consists of a script written in Python which serves as tool for collecting/extracting log files, and resource usage statistics/data for active kubernetes **Pods**, **Nodes**, and get YAML for deployed **DameonSets**. The script is generalised and hence, versalite enough to work with all valid namespaces provided by a user in form of a user input for all kubernetes clusters that use **kubectl** as the command line utility. 

# Pre-requisites:

  * Google Cloud Platform (GCP) subscription, along with access to Google Kubernetes Engine (GKE)
  * GCP SDK or access to Cloud Shell to perform CLI operations
  * Access to the [Prisma Compute Console](https://docs.prismacloud.io/en/enterprise-edition/content-collections/runtime-security/runtime-security) (Optional)

# Working:

* I have used GKE in order to test this tool, however, the tool works with all platforms that use “kubectl”. Navigating to GCP > Kubernetes engine > Clusters
 
  <img width="492" alt="Screenshot 2025-05-03 at 2 34 29 PM" src="https://github.com/user-attachments/assets/c18346bc-d988-4c5c-9d87-98907e15eb70" />

  
* Click on the Connect to the cluster to copy the gcloud command-line access command in order to connect to the cluster using the terminal (first ensure that gcloud SDK is installed locally)

    <img width="536" alt="Screenshot 2025-05-03 at 2 35 13 PM" src="https://github.com/user-attachments/assets/2d827ddf-c921-40d8-9d77-a371cd666671" />


* Listing the active pods in the **kube-system** namespace and **twistlock** namespace

    <img width="538" alt="Screenshot 2025-05-03 at 2 35 36 PM" src="https://github.com/user-attachments/assets/ddae8915-a832-4a69-9962-ec0fe7526719" />
    <img width="540" alt="Screenshot 2025-05-03 at 2 36 10 PM" src="https://github.com/user-attachments/assets/8d2211a1-0f6f-4d81-9cac-0583083724a7" />


* Once we run the script it should ask for a user input for **namespace**. The namespace if invalid, will display the exact error message from the terminal’s output. Now, listing down the available namespace in the cluster  
    <img width="499" alt="Screenshot 2025-05-03 at 2 37 35 PM" src="https://github.com/user-attachments/assets/ebbcbc2a-e9b3-43b3-995f-f2bf0a99f56b" />

* Starting with a non-twistlock namespace which has a few pods running in it, **ns: gmp-system**
  **Note:** The emphasis on a **non-twistlock namespace** is provided because the tool has an additional capability when working with pods in the **twistlock** namespace

  <img width="495" alt="Screenshot 2025-05-03 at 2 44 07 PM" src="https://github.com/user-attachments/assets/69cd6869-7b8f-4e02-a8eb-307000463a57" />

  As soon as the script runs, it will display the pods that it works with in order, finally displaying that it zipped all the results in a zip file.

  The unzipped directory contains subdirectories named on pod names in order to arrange the results of specific pods to be present in a subdirectory named on it’s hostname and a text file containing the output about the resource usage of all nodes (top command) in the cluster is generated.

  <img width="497" alt="Screenshot 2025-05-03 at 2 45 09 PM" src="https://github.com/user-attachments/assets/88af5a16-2492-47ba-ad93-6ffe377231e4" />

  The sub-directories contain the pod logs (kubectl logs) and pod resource usage information (kubectl top) for this particular pod only.   

  <img width="497" alt="Screenshot 2025-05-03 at 2 45 50 PM" src="https://github.com/user-attachments/assets/ea14c2d0-e98d-4baa-af21-b69808e7cd28" />


* The twistlock namespace has an additional capability wherein, the script gathers twistlock logs from within the twistlock pods (kubectl exec..), along with the YAML file of the twistlock Defender daemonset on top of the pod logs, and pod resource usage seen in the previous example

  <img width="498" alt="Screenshot 2025-05-03 at 2 46 46 PM" src="https://github.com/user-attachments/assets/4e6d68d6-79b7-494e-b0ec-a2a72560fdde" />

  The sub-directories contains the .log file or the Defender logs (usually available for export on the Prisma Console UI) along with pod logs and pod usage text file     

  <img width="498" alt="Screenshot 2025-05-03 at 2 47 15 PM" src="https://github.com/user-attachments/assets/ff531c3c-aea7-4c1c-889b-fa51b4f26704" />



# Impact
The usage of this script significantly reduces manual effort (90% or more) which in turns leads to efficient troubleshooting/investigation of technical issues related to the cluster. The script can also be used to keep daily check of the clusters by pulling critical data like resource usage and statistics.

# Roadmap
The tool has just began, left with much more to add in terms of it's capabilities, listing few ideas below:
  * Collecting data for other Kuberntetes resources like active services, secrets, and more
  * If needed, created a simple UI for this tool for smoother access
  * More capabilities in terms of [Prisma Compute Defender](https://docs.prismacloud.io/en/compute-edition/33/admin-guide/install/deploy-defender/defender-types) like getting usueful data about Registry images scans
 
Please feel free to help me with any useful suggestions (open to contributions) you might have for me in order to improve this tool, and simplify daily operations tasks.

# Project status:
I am trying to add more features, optimize the flow, while keeping it in a usable state ALWAYS 

