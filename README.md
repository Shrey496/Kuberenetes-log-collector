# Kubernetes log collector

# Description: 
This project consists of a script written in Python which serves tool  

# Working:

* I have used GKE in order to test this tool, however, the tool works with all platforms that use “kubectl”. Navigating to GCP > Kubernetes engine > Clusters
 
  <img width="492" alt="Screenshot 2025-05-03 at 2 34 29 PM" src="https://github.com/user-attachments/assets/c18346bc-d988-4c5c-9d87-98907e15eb70" />

  
* Click on the Connect to the cluster to copy the gcloud command-line access command in order to connect to the cluster using the terminal (first ensure that gcloud SDK is installed locally)

    <img width="536" alt="Screenshot 2025-05-03 at 2 35 13 PM" src="https://github.com/user-attachments/assets/2d827ddf-c921-40d8-9d77-a371cd666671" />


* Listing the active pods in the *kube-system* namespace and “twistlock” namespace

    <img width="538" alt="Screenshot 2025-05-03 at 2 35 36 PM" src="https://github.com/user-attachments/assets/ddae8915-a832-4a69-9962-ec0fe7526719" />
    <img width="540" alt="Screenshot 2025-05-03 at 2 36 10 PM" src="https://github.com/user-attachments/assets/8d2211a1-0f6f-4d81-9cac-0583083724a7" />


* Once we run the script it should ask for a user input for namespace. The namespace if invalid, will display the exact error message from the terminal’s output. Now, listing down the available namespace in the cluster  
    <img width="499" alt="Screenshot 2025-05-03 at 2 37 35 PM" src="https://github.com/user-attachments/assets/ebbcbc2a-e9b3-43b3-995f-f2bf0a99f56b" />

* Starting with a non-twistlock namespace which has a few pods running in it, ns: gmp-system
  Note: The emphasis on a non-twistlock namespace is provided because the tool has additional capability when working with pods in the twistlock namespace

  As soon as the script runs, it will display the pods that it works with in order, finally displaying that it zipped all the results in a zip file.

  The unzipped directory contains subdirectories named on pod names in order to arrange the results of specific pods to be present in a subdirectory named on it’s hostname and a text file containing the output about the resource usage of all nodes (kubectl top) in the cluster is generated.


The sub-directories contain the pod logs (kubectl logs) and pod resource usage information (kubectl top) for this particular pod only.   

The twistlock namespace has an additional capability wherein, the script gathers twistlock logs from within the twistlock pods (kubectl exec..), along with the YAML file of the twistlock Defender daemonset on top of the pod logs, and pod resource usage seen in the previous example    The sub-directories contains the .log file or the Defender logs (usually available for export on the Prisma Console UI) along with pod logs and pod usage text file     




Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.
Contributing
State if you are open to contributions and what your requirements are for accepting them.
For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.
You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.
Authors and acknowledgment
Show your appreciation to those who have contributed to the project.
License
For open source projects, say how it is licensed.
Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

