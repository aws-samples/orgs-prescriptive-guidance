#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
* Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
* SPDX-License-Identifier: MIT-0
*
* Permission is hereby granted, free of charge, to any person obtaining a copy of this
* software and associated documentation files (the "Software"), to deal in the Software
* without restriction, including without limitation the rights to use, copy, modify,
* merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
* permit persons to whom the Software is furnished to do so.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
* INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
* PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
* HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
* OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
* SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import time
from typing import TYPE_CHECKING

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext
import boto3
from crhelper import CfnResource

if TYPE_CHECKING:
    from mypy_boto3_cloudformation import CloudFormationClient
    from mypy_boto3_iam import IAMClient
    from mypy_boto3_organizations import OrganizationsClient

logger = Logger(utc=True, use_rfc3339=True)
helper = CfnResource(
    json_logging=True,
    log_level="INFO",
    boto_level="CRITICAL",
    sleep_on_delete=120,
    ssl_verify=None,
)

cloudformation: "CloudFormationClient" = boto3.client("cloudformation")
iam: "IAMClient" = boto3.client("iam")
organizations: "OrganizationsClient" = boto3.client(
    "organizations",
    region_name="us-east-1",
    endpoint_url="https://organizations.us-east-1.amazonaws.com",
)

try:
    root_id = os.getenv("ROOT_ID")
except Exception as e:
    helper.init_failure(e)

policy_types = {
    "AISERVICES_OPT_OUT_POLICY",
    "BACKUP_POLICY",
    "CHATBOT_POLICY",
    "RESOURCE_CONTROL_POLICY",
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY",
}


@helper.create
def create(event: dict, context: LambdaContext):
    response = cloudformation.describe_organizations_access(CallAs="SELF")
    status: str = response.get("Status")
    logger.info("Organizations Access Status: " + status)

    if status == "ACTIVE":
        logger.warn("Organizations access is already active")
    else:
        logger.debug("Activating organizations access...")
        cloudformation.activate_organizations_access()
        logger.info("Successfully activated organizations access")

    for policy_type in policy_types:
        logger.debug(f"Enabling {policy_type} policy type...")
        while True:
            try:
                organizations.enable_policy_type(RootId=root_id, PolicyType=policy_type)
            except organizations.exceptions.PolicyTypeAlreadyEnabledException:
                break
            except organizations.exceptions.ConcurrentModificationException:
                time.sleep(0.1)
            else:
                break
        logger.info(f"Enabled {policy_type} policy type")

    logger.debug("Enabling AWS service access for IAM...")
    organizations.enable_aws_service_access(ServicePrincipal="iam.amazonaws.com")
    logger.info("Enabled AWS service access for IAM")

    logger.debug("Enabling organizations root credentials management...")
    iam.enable_organizations_root_credentials_management()
    logger.info("Enabled organizations root credentials management")

    logger.debug("Enabling organizations root sessions...")
    iam.enable_organizations_root_sessions()
    logger.info("Enabled organizations root sessions")


@helper.delete
def delete(event: dict, context: LambdaContext):
    response = cloudformation.describe_organizations_access(CallAs="SELF")
    status: str = response.get("Status")
    logger.info("Organizations Access Status: " + status)

    if status == "DISABLED":
        logger.warn("Organizations access is already disabled")
    else:
        logger.debug("Deactivating organizations access...")
        cloudformation.deactivate_organizations_access()
        logger.info("Successfully deactivated organizations access")

    for policy_type in policy_types:
        logger.debug(f"Disabling {policy_type} policy type...")
        while True:
            try:
                organizations.disable_policy_type(
                    RootId=root_id, PolicyType=policy_type
                )
            except organizations.exceptions.PolicyTypeNotEnabledException:
                break
            except organizations.exceptions.ConcurrentModificationException:
                time.sleep(0.1)
            else:
                break
        logger.info(f"Disabled {policy_type} policy type")

    logger.debug("Disabling organizations root sessions...")
    iam.disable_organizations_root_sessions()
    logger.info("Disabled organizations root sessions")

    logger.debug("Disabling organizations root credentials management...")
    iam.disable_organizations_root_credentials_management()
    logger.info("Disabled organizations root credentials management")

    logger.debug("Disabling AWS service access for IAM...")
    organizations.disable_aws_service_access(ServicePrincipal="iam.amazonaws.com")
    logger.info("Disabled AWS service access for IAM")


@logger.inject_lambda_context(log_event=True)
def handler(event: dict, context: LambdaContext) -> dict:
    helper(event, context)
