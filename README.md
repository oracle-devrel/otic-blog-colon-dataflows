# otic-blog-colon-dataflows

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_otic-blog-colon-dataflows)](https://sonarcloud.io/dashboard?id=oracle-devrel_otic-blog-colon-dataflows)

## Introduction

This code is part of a soon to be released blog in the "Behind the Scenes with OCI Engineering" series https://blogs.oracle.com/cloud-infrastructure/category/oci-behind-the-scenes

The example contained within gives users of OCI DataFlow the ability to ingest objects with colon characters ":" with greater ease than before. 


## Getting Started

To get started with OCI DataFlow's it is recommended to read review https://docs.oracle.com/en-us/iaas/data-flow/using/dfs_getting_started.htm. 

- For additional information we recommend you read the blog post related to this repo once published (it will be linked to here).
- For information regarding OCI Audit Logs review https://docs.oracle.com/en-us/iaas/Content/Logging/Concepts/audit_logs.htm.

## Prerequisites

1. This demo code requires that the logs be available in an OCI Object Storage bucket. For information on exporting OCI Audit Logs to OCI Object Storage review https://docs.oracle.com/en-us/iaas/Content/connector-hub/archivelogs.htm

2. The example PySpark script includes cross tenancy OCI Object Storage access. If this matches your scenario you will need to setup sufficent policies see https://docs.oracle.com/en-us/iaas/Content/Object/Concepts/accessingresourcesacrosstenancies.htm 

3. The DataFlow will require an OCI Object Storage bucket to write results as well as other runtime logs, see https://docs.oracle.com/en-us/iaas/data-flow/using/set-up-iam-policies.htm for setting up DataFlow policies. 

4. A pre-packaged archive.zip file with the Colon Filesystem is in this repo. Steps to build from source can be found here https://docs.oracle.com/en-us/iaas/data-flow/using/third-party-provide-archive.htm.

## Simple archive.zip build steps

If you want to skip this, there is an archive.zip package in the repo. You will need to upload the archive.zip to OCI object storage and reference in your DataFlow application e.g. oci://bucket@namespace/archive.zip. 

The source code in ./colonfs has been packaged into a jar "oci-hdfs-colon-connector-1.0.0.jar" in ./build/java. To package into an archive.zip simply execute the following commands. 

```
cd ./build

zip -r archive.zip java version.txt
```

If you require pandas or other python3 dependancies you follow the steps here https://docs.oracle.com/en-us/iaas/data-flow/using/third-party-provide-archive.htm  


## Notes/Issues

- Tested using Spark 3.2.1 and Python 3.8

## Contributing
This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

## License
Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 