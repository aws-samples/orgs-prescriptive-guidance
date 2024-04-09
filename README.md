# Guidance for Organization on AWS 

### Table of contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Tools and services](#tools-and-services)
4. [Usage](#usage)
5. [Use Cases](#use-cases)
6. [Clean up](#clean-up)
7. [Reference](#reference)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction

This repository contains a collection of [AWS CloudFormation](https://aws.amazon.com/cloudformation/) templates to create up an [AWS Organizations](https://aws.amazon.com/organizations/) structure.

## Prerequisites

- [Python 3](https://www.python.org/downloads/), installed
- [AWS Command Line Interface (AWS CLI)](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) version 2, installed
- [AWS Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html), installed

## Tools and services

- [AWS SAM](https://aws.amazon.com/serverless/sam/) - The AWS Serverless Application Model (SAM) is an open-source framework for building serverless applications. It provides shorthand syntax to express functions, APIs, databases, and event source mappings.
- [AWS Control Tower](https://aws.amazon.com/controltower/) - AWS Control Tower provides the easiest way to set up and govern a secure, multi-account AWS environment, called a landing zone.
- [AWS Organizations](https://aws.amazon.com/organizations/) - AWS Organizations helps you centrally manage and govern your environment as you grow and scale your AWS resources.
- [AWS Service Catalog](https://aws.amazon.com/servicecatalog/) - AWS Service Catalog allows organizations to create and manage catalogs of IT services that are approved for use on AWS.

## Usage

#### Parameters

| Parameter                |  Type  |         Default          | Description          |
| ------------------------ | :----: | :----------------------: | -------------------- |
| pSSOInstanceId           | String |  _None_  | Optional - AWS IAM Identity Center instance ID |
| pDeveloperPrefix         | String | app | Prefix used by developers when creating IAM roles and CloudFormation stacks |
| pCloudFormationRoleName  | String | CloudFormationRole | Name of the IAM role used by AWS CloudFormation |
| pServiceCatalogRoleName  | String | ServiceCatalogRole | Name of the IAM role used by AWS Service Catalog |
| pBreakGlassAdminRoleName | String | BreakGlassAdministratorRole | Name of the IAM role used by administrators in the event of an emergency |
| pRegions                 | String | us-east-1 | Comma-delimited list of AWS Regions |
| pSandboxOuName           | String | Sandbox | Name of the organizational unit for sandbox AWS accounts |
| pSecurityOuName          | String | Security_Prod | Name of the organizational unit for security-related AWS accounts |

#### Installation

To deploy the template, you first need to install the [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (AWS SAM).

```
git clone https://github.com/aws-samples/orgs-prescriptive-guidance
cd orgs-prescriptive-guidance
sam build
sam deploy \
  --guided \
  --tags "GITHUB_ORG=aws-samples GITHUB_REPO=orgs-prescriptive-guidance"
```

## Use Cases

#### To Access an EC2 Instance

After installing the AWS CLI, install the [AWS Systems Manager Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html
).

```bash
aws sso login --profile <profile-name>
aws --profile <profile-name> ssm start-session --target <instance-id> --document-name SSM-SessionManagerRunShell
```

## Clean up

Deleting the CloudFormation Stack will remove the CloudFormation StackSets and IAM Identity Center Permission Sets, but it will retain the AWS Organizations.

```
sam delete
```

## Reference

This solution is inspired by these references:

- [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/architecture.html)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

