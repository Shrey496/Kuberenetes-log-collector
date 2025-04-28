#Collect pod details function to check for pod logs
#Directory structure to avoid redundant code
#zip files function

import os
import subprocess
import json
import zipfile

# Define output directories
OUTPUT_DIR = "Diagnostics"
NAMESPACE = input("Enter the namespace: ")

def run_kubectl_command(command):
    """Run a kubectl command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # result.returncode -- exit status of the process (0 for success, nonzero for failure)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr.strip()}"
    
#To check if the namespace is valid, if not, return the exact error message as seen on the UI
def namespace_exists():
    result = run_kubectl_command(f"kubectl get ns {NAMESPACE}")
    if "Error" in result:
        print(result)
        return False
    else:
        return True

# Retrieve all pods from the mentioned namespace
def get_pods():
    pods_json = run_kubectl_command(f"kubectl get pods -n {NAMESPACE} -o json")
    
    try:
        pod_list = []
       
       #converting json to a dictionary
        pod_data = json.loads(pods_json)
        
        #parsing the dictionary
        for p in pod_data["items"]:
            if p["metadata"]["name"]:
                pod_list.append(p["metadata"]["name"])
        
        return pod_list
    
    except json.JSONDecodeError:
        print("Error parsing pod JSON data")
        return []

#Collect pod details with the help of common kubectl commands  
def collect_pod_details(pod_name):

    pod_info = {
        "describe": run_kubectl_command(f"kubectl describe pod {pod_name} -n {NAMESPACE}"),
        # "logs": run_kubectl_command(f"kubectl logs {pod_name} -n {NAMESPACE}"),
    }
    pod_json = run_kubectl_command(f"kubectl get pod {pod_name} -n {NAMESPACE} -o json")
    
    # if pod_json.startswith("Error"):
    #     return pod_info

    #Extracting node name, pod ip, and events as output from the describe pod command
    try:
        pod_data = json.loads(pod_json)
        pod_info["node_name"] = pod_data["spec"]["nodeName"]
        pod_info["pod_ip"] = pod_data["status"].get("podIP", "N/A")
        pod_info["events"] = run_kubectl_command(f"kubectl get events -n {NAMESPACE} --field-selector involvedObject.name={pod_name}")

    except json.JSONDecodeError:
        print(f"Error parsing JSON data for pod {pod_name}")

    return pod_info

#Retrieving the YAML file for the twistlock namespace.
#ONLY EXECUTED if namespace is twistlock
def get_twistlock_daemonset():
    ds_yaml = run_kubectl_command(f"kubectl get ds -n {NAMESPACE} -o yaml")
    with open(os.path.join(OUTPUT_DIR, "twistlock_daemonset.yaml"), "w") as f:
        f.write(ds_yaml)

#Identify if it is a defender or a console twistlock pod, and Exec into the pod to download defender.log or console.log. 
#ONLY EXECUTED if namespace is twistlock
def exec_into_pod_and_fetch_logs(pod_name):
  
    if "defender" in pod_name:
        log_type = 'defender'
    elif "console" in pod_name:
        log_type = 'console'
    LOGS_DIR = os.path.join(OUTPUT_DIR, pod_name)
    os.makedirs(LOGS_DIR, exist_ok=True)
        
    #The logs will be stored in the resepctive directories created for pods.
    log_path = f"/var/lib/twistlock/log/{log_type}.log"
    local_path = os.path.join(LOGS_DIR, f"{pod_name}_{log_type}.log")
    
     # Run kubectl exec and capture the log file.
    command = f"kubectl exec {pod_name} -n {NAMESPACE} -- cat {log_path} > {local_path}"  
    subprocess.run(command, shell=True, check=False)  

#Get Pod logs and store it within the directory created for each pod.
def pod_logs(pod_name):
    LOGS_DIR = os.path.join(OUTPUT_DIR, pod_name)
    os.makedirs(LOGS_DIR, exist_ok=True)

    local_path = os.path.join(LOGS_DIR, f"{pod_name}.log")
    logs_pod = run_kubectl_command(f"kubectl logs {pod_name} -n {NAMESPACE} > {local_path}")

#Check resource capacity and usage of individual pods and nodes using the 'top' command.
def check_resources(pod_name):
    node_resources = {
        "node_resources": run_kubectl_command("kubectl top nodes"),
        "network_info": run_kubectl_command("kubectl get nodes -o wide")  
    }
    
    LOGS_DIR = os.path.join(OUTPUT_DIR, pod_name)
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    pod_resources = {
    "pod_stats": run_kubectl_command(f"kubectl get pod {pod_name} -o wide -n {NAMESPACE}"),
    "pod_resources": run_kubectl_command(f"kubectl top pod {pod_name} -n {NAMESPACE}")
    }
    
    #The top command output will be stored within the main "Diagnostics" directory.
    with open(os.path.join(OUTPUT_DIR, "nodes_resource_usage.txt"),  "w") as f:
        for key, value in node_resources.items():
            f.write(f"\n=== {key} ===\n{value}\n")

    #The top command output relevant to the pod will be stored within the pod's directory alongside pod logs.
    with open(os.path.join(LOGS_DIR, "pod_resource_usage.txt"), "w") as f:
        for key, value in pod_resources.items():
            f.write(f"\n=== {key} ===\n{value}\n")


# def zip_results():
#     """Zip all collected data"""
#     zip_filename = "twistlock_diagnostics.zip"
#     with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
#         for root, _, files in os.walk(OUTPUT_DIR):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 zipf.write(file_path, os.path.relpath(file_path, OUTPUT_DIR))
#     print(f"Zipped all results into {zip_filename}")

def main():
    
    #Check if the namespace input is valid
    if namespace_exists():
    
        #Get the pods in the namespace
        twistlock_pods = get_pods()
        if not twistlock_pods:
            print("No pods found in the mentioned namespace.")
            return
        for pod in twistlock_pods:
            print(f"Processing pod: {pod}")
            pod_info = collect_pod_details(pod)

            #If namespace is twistlock, only then execute the logs and daemonset function because we know both would exist for twistlock resources.
            if NAMESPACE == "twistlock":
                exec_into_pod_and_fetch_logs(pod)
                get_twistlock_daemonset()
            check_resources(pod)
            pod_logs(pod)
        # zip_results()
if __name__ == "__main__":
    main()