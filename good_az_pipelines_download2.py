import subprocess
import os
import zipfile
import sys
import shutil

# -----------------------------------
# Synapse configuration
# -----------------------------------
workspace_name = "ayadatawh"
resource_group = "CustomerInsightsProd"
output_folder = "synapse_pipelines_json"
zip_file_name = "synapse_pipelines_json.zip"

az_cli = None


# -----------------------------------
# Find Azure CLI
# -----------------------------------
def find_azure_cli():

    global az_cli

    print("Searching for Azure CLI...")

    az_path = shutil.which("az")

    if az_path:
        az_cli = az_path
        print(f"Azure CLI found: {az_cli}")
        return

    possible_path = r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"

    if os.path.exists(possible_path):
        az_cli = possible_path
        print(f"Azure CLI found: {az_cli}")
        return

    print("ERROR: Azure CLI not found.")
    sys.exit(1)


# -----------------------------------
# Azure Login
# -----------------------------------
def azure_login():

    print("Checking Azure login status...")

    result = subprocess.run(
        [az_cli, "account", "show"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        print("Opening Azure login...")

        login = subprocess.run([az_cli, "login"])

        if login.returncode != 0:
            print("Azure login failed.")
            sys.exit(1)

        print("Azure login successful.")

    else:
        print("Already logged into Azure.")


# -----------------------------------
# Get pipeline list
# -----------------------------------
def get_pipeline_list():

    print("Retrieving pipelines...")

    command = [
        az_cli,
        "synapse",
        "pipeline",
        "list",
        "--workspace-name",
        workspace_name,
        "--query",
        "[].name",
        "-o",
        "tsv"
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error retrieving pipelines:")
        print(result.stderr)
        sys.exit(1)

    pipelines = result.stdout.strip().split("\n")

    print(f"Total pipelines found: {len(pipelines)}")

    return pipelines


# -----------------------------------
# Download pipelines
# -----------------------------------
def download_pipelines(pipelines):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pipeline in pipelines:

        if pipeline.strip() == "":
            continue

        print(f"Downloading pipeline: {pipeline}")

        command = [
            az_cli,
            "synapse",
            "pipeline",
            "show",
            "--workspace-name",
            workspace_name,
            "--name",
            pipeline
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Failed to download {pipeline}")
            continue

        file_path = os.path.join(output_folder, f"{pipeline}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result.stdout)


# -----------------------------------
# Create ZIP
# -----------------------------------
def create_zip():

    print("Creating ZIP file...")

    with zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED) as zipf:

        for root, dirs, files in os.walk(output_folder):

            for file in files:

                full_path = os.path.join(root, file)

                zipf.write(full_path, os.path.basename(full_path))

    print(f"ZIP created: {zip_file_name}")


# -----------------------------------
# Main
# -----------------------------------
def main():

    find_azure_cli()

    azure_login()

    pipelines = get_pipeline_list()

    download_pipelines(pipelines)

    create_zip()

    print("Process completed successfully.")


if __name__ == "__main__":
    main()
