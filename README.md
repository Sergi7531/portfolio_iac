# **Portfolio as Code**

## **Contents**
- [Abstract](#abstract)
- [Motivation](#motivation)
- [Specification](#specification)
- [Reference Implementation](#reference-implementation)

---

## **Abstract**
This document outlines the deployment of a personal portfolio in the AWS Cloud using an Infrastructure as Code (IaC) approach with AWS CDK. 
The portfolio hosts a static website on Amazon S3, distributed securely via Amazon CloudFront, and protected with an SSL certificate issued by AWS Certificate Manager (ACM). 
The project also incorporates a custom domain (managed in AWS Route 53), which was originally registered through an external provider.
The implementation ensures secure and efficient content delivery by leveraging AWS (free!) services, while maintaining flexibility for future updates and scalability.

Note: This project is absolutely free to deploy, as it leverages the AWS Free Tier services. Still, it is recommended to monitor the usage to avoid any unexpected charges. It is highly recommended to setup a budget alarm in the AWS Billing Dashboard to avoid any unexpected charges.
---

## **Motivation**
A personal portfolio serves as a professional showcase, and by leveraging AWS services, this project achieves:
- **Cost efficiency**: Static hosting on S3 minimizes expenses while providing high availability.
- **Security**: CloudFront + ACM ensures HTTPS encryption and protects content access to a secure HTTPS protocol.
- **Performance**: CloudFront’s global structure accelerates content delivery via caching content in edge locations.
- **Custom Domain Support**: The portfolio is accessible via a personalized domain, enhancing professional branding.
- **Infrastructure as Code (IaC)**: The deployment is automated and maintainable using AWS CDK.
- And most importantly, skills in AWS services and IaC best practices.

This architecture ensures: a high-performance, secure, and scalable solution for the hosting.

---

## **Specification**
### **Architecture Overview**
The deployment consists of the following AWS components:

- **Amazon S3**: Acts as the origin for hosting static website assets.
- **Amazon CloudFront**: Distributes the website globally with caching and SSL termination.
- **AWS Certificate Manager (ACM)**: Provides an SSL/TLS certificate for secure HTTPS communication.
- **AWS Route 53**: Manages the custom domain name and DNS routing.
- **AWS CDK (Python)**: Defines and deploys the infrastructure as code.

### **Domain Management**
The project uses an externally registered domain, imported into Route 53 for DNS resolution. 
However, the domain itself is **not provisioned via AWS CDK** due to its external origin. 

The domain was originally purchased using NameCheap services, and although the portfolio was initially hosted using another provider, 
the migration to AWS Cloud was motivated by the benefits of scalability, **security**, and cost efficiency.

### **Security Measures**
- **CloudFront Origin Access Identity (OAI)**: This ensures that the S3 bucket is accessible only through CloudFront, preventing direct access.
- **HTTPS enforcement**: Providing CloudFront with an ACM-issued public certificate to assure in-transit encryption.
- **IAM Policies**: This security layer restrict the S3 bucket access **only** to CloudFront’s origin identity. This is mainly focused on having an AWS WAF to protect the website from common web exploits and Denial of Service attacks. As said before, this project is leveraged using the AWS Free Tier, so that security layer is not implemented. 

---

## **Reference Implementation**
The following summarizes the CDK implementation:

1. **S3 Bucket**: Configured as a private storage for static assets.
2. **CloudFront Distribution**:
   - Uses the S3 bucket as its origin.
   - Enforces HTTPS via ACM.
   - Restricts S3 bucket access using an Origin Access Identity (OAI).
3. **ACM Certificate**:
   - Issued in `us-east-1` for CloudFront compatibility.
   - Validated via Route 53 DNS records.
4. **Route 53 Alias Record**:
   - Maps the custom domain (`sergidominguez.com`) to the CloudFront distribution.
5. **Deployment Process**:
   - First, bootstrap your AWS account:region (in case you haven't yet!):
   > cdk bootstrap aws://<your_account_number>/<your_region>
   - Deploy the infrastructure to your AWS account using the 'deploy' command:
   > cdk deploy
   
This process ensures an automated and reliable deployment, leveraging AWS best practices for security, performance, and scalability.
The process also provides a clear and structured overview of the project, ensuring maintainability and clarity for future improvements.
By deploying with CDK, this project leverages "Change sets", which allow the changes summary before deploying them. 
This feature ensures the correct changes are about to be deployed (and therefore applied) to the infrastructure.

