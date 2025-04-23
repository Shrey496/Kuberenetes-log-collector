import os
import subprocess
import json
import zipfile

# Define output directories
OUTPUT_DIR = "twistlock_diagnostics"
NAMESPACE = "twistlock"
def run_kubectl_command(command):
    """Run a kubectl command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # result.returncode -- exit status of the process (0 for success, nonzero for failure)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr.strip()}"
def get_twistlock_pods():
    """Retrieve all pods in the twistlock namespace"""
    pods_json = run_kubectl_command(f"kubectl get pods -n {NAMESPACE} -o json")
    #print("Printing from the get_twistlock_pods function -- pods_json: ", pods_json)
    try:
        pod_list = []
        #converting json to a dictionary
        pod_data = json.loads(pods_json)
        #parsing the dictionary
        for p in pod_data["items"]:
            if p["metadata"]["name"].startswith(NAMESPACE):
                pod_list.append(p["metadata"]["name"])
        return pod_list
    except json.JSONDecodeError:
        print("Error parsing pod JSON data")
        return []
    
def collect_pod_details(pod_name):
    """Get describe, logs, node name, pod IP, and events"""
    pod_info = {
        "describe": run_kubectl_command(f"kubectl describe pod {pod_name} -n {NAMESPACE}"),
        "logs": run_kubectl_command(f"kubectl logs {pod_name} -n {NAMESPACE}"),
    }
    pod_json = run_kubectl_command(f"kubectl get pod {pod_name} -n {NAMESPACE} -o json")
    if pod_json.startswith("Error"):
        return pod_info
    try:
        pod_data = json.loads(pod_json)
        pod_info["node_name"] = pod_data["spec"]["nodeName"]
        pod_info["pod_ip"] = pod_data["status"].get("podIP", "N/A")
        pod_info["events"] = run_kubectl_command(f"kubectl get events -n {NAMESPACE} --field-selector involvedObject.name={pod_name}")
    except json.JSONDecodeError:
        print(f"Error parsing JSON data for pod {pod_name}")
    return pod_info
def get_twistlock_daemonset():
    """Retrieve YAML for the active Twistlock daemonset"""
    ds_yaml = run_kubectl_command(f"kubectl get ds -n {NAMESPACE} -o yaml")
    with open(os.path.join(OUTPUT_DIR, "twistlock_daemonset.yaml"), "w") as f:
        f.write(ds_yaml)
def exec_into_pod_and_fetch_logs(pod_name):
    """Identify if defender or console pod, and Exec into the pod to download defender.log or console.log"""
    # Run kubectl exec and capture the log file
    if "defender" in pod_name:
        log_type = 'defender'
    elif "console" in pod_name:
        log_type = 'console'
    LOGS_DIR = os.path.join(OUTPUT_DIR, pod_name)
    os.makedirs(LOGS_DIR, exist_ok=True)
        
    log_path = f"/var/lib/twistlock/log/{log_type}.log"
    local_path = os.path.join(LOGS_DIR, f"{pod_name}_{log_type}.log")
    
    #cat will copy the contents of the provided log_path to the filepath created (localpath)
    command = f"kubectl exec {pod_name} -n {NAMESPACE} -- cat {log_path} > {local_path}"  
    subprocess.run(command, shell=True, check=False)        
def check_resources(pod_name):
    """Check resource capacity and usage of individual pods and nodes"""
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
    
    with open(os.path.join(OUTPUT_DIR, "nodes_resource_usage.txt"),  "w") as f:
        for key, value in node_resources.items():
            f.write(f"\n=== {key} ===\n{value}\n")

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
    #Get the pods in the namespace
    twistlock_pods = get_twistlock_pods()
    if not twistlock_pods:
        print("No twistlock pods found in the namespace.")
        return 
    for pod in twistlock_pods:
        print(f"Processing pod: {pod}")
        pod_info = collect_pod_details(pod)
       
        # Save pod details to JSON file
        # with open(os.path.join(LOGS_DIR, f"{pod}_details.json"), "w") as f:
        #     json.dump(pod_info, f, indent=4)
        exec_into_pod_and_fetch_logs(pod)
        check_resources(pod)
    get_twistlock_daemonset()
    # zip_results()
if __name__ == "__main__":
    main()
