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
| pRegions                 | String | us-east-1 | Comma-delimited list of AWS Regions |
| pSandboxOuName           | String | Sandbox | Name of the organizational unit for sandbox AWS accounts |
| pSecurityOuName          | String | Security_Prod | Name of the organizational unit for security-related AWS accounts |

#### Installation

To deploy the template, you first need to install the [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) (AWS SAM).

```bash
git clone https://github.com/aws-samples/orgs-prescriptive-guidance
cd orgs-prescriptive-guidance
aws --region us-east-1 cloudformation deploy \
  --template-file github_ci_template.yml \
  --stack-name orgs-prescriptive-guidance-cicd \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

aws --region us-east-1 cloudformation describe-stacks --stack-name orgs-prescriptive-guidance-cicd --query "Stacks[0].Outputs"
```

Then, follow this [guide](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#creating-configuration-variables-for-a-repository) to create GitHub Action variables in the repository:

* `ARTIFACT_BUCKET` = value of `oArtifactBucket` from above
* `ASSUME_ROLE_ARN` = value of `oGitHubRoleArn` from above
* `CF_ROLE_ARN` = value of `oCloudFormationRoleArn` from above

The variables should look like the image below:

![GitHub Action Variables](./docs/github_actions_variables.png)

## Use Cases

#### Emergency Access

In the event that there are any issues with AWS IAM Identity Center, IAM users `EmergencyAccess_RO` and `EmergencyAccess_Ops` have been deployed in the management account. These users can assume IAM roles `EmergencyAccess_RO` and `EmergencyAccess_Ops` in every account. These users thus have privileged access to all accounts which necessitates that they be used sparingly in a secure manner.

There are no credentials associated with these users. To set credentials, and enable multi-factor authentication for these users, follow these [instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable.html) to configure MFA devices for each EmergencyAccess user.

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

