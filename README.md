# AWS Inventory Checker

This Python script checks the inventory of your AWS EC2 instances across multiple regions to determine if the "xz-utils" package is installed. It then generates a CSV report with the results.

## Prerequisites

- Python 3.x installed on your system
- AWS CLI configured with appropriate access credentials
- Boto3 library installed (`pip install boto3`)

## Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/aws-inventory-checker.git
```

2. Navigate to the cloned directory:
```bash
cd aws-inventory-checker
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
# Usage
Set the environment variables for the regions and application required
```bash
export REGIONS=eu-west-1,eu-central-1,us-east-1,eu-west-2
export FILTER_VALUES=xz-utils
```

Run the script:
```bash
python inventory_checker.py
```

3. Once the script completes execution, you'll find the generated CSV report named output.csv in the same directory. It will also print out the output for each instance
