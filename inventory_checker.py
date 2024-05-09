import os
import boto3
import csv

# Read regions from environment variable
regions_str = os.getenv('REGIONS', 'eu-west-1,eu-central-1,us-east-1,eu-west-2')
regions = regions_str.split(',')

# Read filter values from environment variable
filter_values_str = os.getenv('FILTER_VALUES', 'xz-utils')
filter_values = filter_values_str.split(',')

# Open CSV file in write mode
with open('output.csv', 'w', newline='') as csvfile:
    # Define CSV writer
    csv_writer = csv.writer(csvfile)
    # Write header row
    csv_writer.writerow(['Region', 'Instance ID', 'Package ID'])

    # Loop through regions
    for region in regions:
        # Initialize Boto3 EC2 client for the region
        ec2_client = boto3.client('ec2', region_name=region)
        # Initialize Boto3 Systems Manager (SSM) client for the region
        ssm_client = boto3.client('ssm', region_name=region)

        # Get instance IDs for Linux instances
        response = ec2_client.describe_instances()

        instance_ids = [instance['InstanceId'] for reservation in response['Reservations'] for instance in reservation['Instances']]

        # Iterate over instance IDs
        for instance_id in instance_ids:
            try:
                # List inventory entries for each instance
                ssm_response = ssm_client.list_inventory_entries(
                    InstanceId=instance_id,
                    TypeName='AWS:Application',
                    Filters=[
                        {
                            'Key': 'Name',
                            'Values': filter_values,
                            'Type': 'Equal'
                        }
                    ]
                )

                # Check if inventory entries exist for specified package(s)
                if 'Entries' in ssm_response and ssm_response['Entries']:
                    # Extract PackageId from the inventory
                    package_id = ssm_response['Entries'][0].get('Version')
                    # Write region, instance ID, and package ID to CSV file
                    csv_writer.writerow([region, instance_id, package_id])
                    print(f"Instance {instance_id} in region {region} has {filter_values} installed with Version: {package_id}")
                else:
                    # Write region, instance ID, and "Package not found" message to CSV file
                    csv_writer.writerow([region, instance_id, f"No {filter_values} found"])
                    print(f"No {filter_values} found in the inventory for instance {instance_id} in region {region}")
            except Exception as e:
                print(f"Error: {e}")
