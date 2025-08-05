# Multi-Agent Workflow Optimization System - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the multi-agent workflow optimization system to AWS using Bedrock, Lambda, API Gateway, S3, and DynamoDB.

## Prerequisites

### Required AWS Services
- AWS Bedrock (Claude 3.5 Sonnet access)
- AWS Lambda
- Amazon API Gateway
- Amazon S3
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch

### Development Environment
- Python 3.11+
- AWS CLI v2
- AWS SAM CLI
- Docker (for local testing)
- Git

### Permissions Required
- AWS Bedrock access with Claude 3.5 Sonnet model permissions
- Lambda function creation and management
- S3 bucket creation and management
- DynamoDB table creation and management
- API Gateway creation and management
- IAM role and policy management
- CloudWatch logs access

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   API Gateway   │────│  Orchestration   │────│   AWS Bedrock   │
│                 │    │     Agent        │    │ Claude 3.5 Sonnet│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌───────┴───────┐              │
         │               │               │              │
    ┌────▼────┐    ┌─────▼─────┐   ┌─────▼─────┐       │
    │ Input   │    │ Analysis  │   │Optimization│       │
    │ Agent   │    │  Agent    │   │   Agent    │       │
    └─────────┘    └───────────┘   └───────────┘       │
         │               │               │              │
         └───────────────┼───────────────┘              │
                         │                              │
                   ┌─────▼─────┐                       │
                   │  Output   │◄──────────────────────┘
                   │  Agent    │
                   └───────────┘
                         │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼───┐        ┌────────▼────────┐      ┌────▼────┐
│   S3  │        │   DynamoDB      │      │Framework│
│ Data  │        │ State Mgmt      │      │Knowledge│
│Storage│        │                 │      │  Base   │
└───────┘        └─────────────────┘      └─────────┘
```

## Pre-Deployment Setup

### 1. Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region, and Output format
```

### 2. Enable AWS Bedrock Access

```bash
# Request access to Claude 3.5 Sonnet model in AWS Bedrock console
# Wait for approval (typically 24-48 hours for new accounts)

# Verify access
aws bedrock list-foundation-models --region us-east-1
```

### 3. Clone and Prepare Repository

```bash
git clone <repository-url>
cd aws_bedrock_deployment

# Install Python dependencies
pip install -r requirements.txt

# Install SAM CLI
# macOS: brew install aws-sam-cli
# Windows: Download from AWS website
# Linux: pip install aws-sam-cli
```

## Infrastructure Deployment

### 1. Create S3 Bucket

```bash
# Create main data bucket
aws s3 mb s3://workflow-optimization-data --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket workflow-optimization-data \
  --versioning-configuration Status=Enabled

# Set up bucket encryption
aws s3api put-bucket-encryption \
  --bucket workflow-optimization-data \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      }
    }]
  }'
```

### 2. Upload Training Data and Knowledge Base

```bash
# Upload training data
aws s3 cp training_data/ s3://workflow-optimization-data/training_data/ --recursive

# Upload framework knowledge
aws s3 cp framework_knowledge/ s3://workflow-optimization-data/framework_knowledge/ --recursive

# Upload validation data
aws s3 cp validation_data/ s3://workflow-optimization-data/validation_data/ --recursive

# Upload BPI Challenge data (if available)
aws s3 cp ../data/ s3://workflow-optimization-data/bpi_challenge_data/ --recursive
```

### 3. Create DynamoDB Tables

```bash
# Create workflow processing state table
aws dynamodb create-table \
  --table-name workflow-processing-state \
  --attribute-definitions \
    AttributeName=session_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
    AttributeName=workflow_id,AttributeType=S \
    AttributeName=processing_stage,AttributeType=S \
  --key-schema \
    AttributeName=session_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --global-secondary-indexes \
    IndexName=workflow-id-index,KeySchema=[{AttributeName=workflow_id,KeyType=HASH},{AttributeName=timestamp,KeyType=RANGE}],Projection='{Type=ALL}',ProvisionedThroughput='{ReadCapacityUnits=5,WriteCapacityUnits=5}' \
    IndexName=processing-stage-index,KeySchema=[{AttributeName=processing_stage,KeyType=HASH},{AttributeName=timestamp,KeyType=RANGE}],Projection='{Type=KEYS_ONLY}',ProvisionedThroughput='{ReadCapacityUnits=5,WriteCapacityUnits=5}' \
  --billing-mode PAY_PER_REQUEST \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES

# Create agent performance metrics table
aws dynamodb create-table \
  --table-name agent-performance-metrics \
  --attribute-definitions \
    AttributeName=agent_name,AttributeType=S \
    AttributeName=metric_timestamp,AttributeType=N \
    AttributeName=session_id,AttributeType=S \
    AttributeName=quality_score,AttributeType=N \
  --key-schema \
    AttributeName=agent_name,KeyType=HASH \
    AttributeName=metric_timestamp,KeyType=RANGE \
  --global-secondary-indexes \
    IndexName=session-metrics-index,KeySchema=[{AttributeName=session_id,KeyType=HASH},{AttributeName=metric_timestamp,KeyType=RANGE}],Projection='{Type=ALL}',ProvisionedThroughput='{ReadCapacityUnits=5,WriteCapacityUnits=5}' \
    IndexName=quality-score-index,KeySchema=[{AttributeName=agent_name,KeyType=HASH},{AttributeName=quality_score,KeyType=RANGE}],Projection='{Type=INCLUDE,NonKeyAttributes=[session_id,metric_timestamp,execution_time_ms]}',ProvisionedThroughput='{ReadCapacityUnits=5,WriteCapacityUnits=5}' \
  --billing-mode PAY_PER_REQUEST

# Create workflow optimization results table
aws dynamodb create-table \
  --table-name workflow-optimization-results \
  --attribute-definitions \
    AttributeName=workflow_id,AttributeType=S \
    AttributeName=optimization_timestamp,AttributeType=N \
    AttributeName=inefficiency_score,AttributeType=N \
    AttributeName=optimization_potential,AttributeType=N \
  --key-schema \
    AttributeName=workflow_id,KeyType=HASH \
    AttributeName=optimization_timestamp,KeyType=RANGE \
  --global-secondary-indexes \
    IndexName=inefficiency-score-index,KeySchema=[{AttributeName=inefficiency_score,KeyType=HASH},{AttributeName=optimization_timestamp,KeyType=RANGE}],Projection='{Type=INCLUDE,NonKeyAttributes=[workflow_id,optimization_potential,session_id]}',ProvisionedThroughput='{ReadCapacityUnits=5,WriteCapacityUnits=5}' \
  --billing-mode PAY_PER_REQUEST

# Create system configuration table
aws dynamodb create-table \
  --table-name system-configuration \
  --attribute-definitions \
    AttributeName=config_category,AttributeType=S \
    AttributeName=config_key,AttributeType=S \
  --key-schema \
    AttributeName=config_category,KeyType=HASH \
    AttributeName=config_key,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
```

### 4. Create IAM Roles and Policies

```bash
# Create execution role for Lambda functions
aws iam create-role \
  --role-name lambda-execution-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# Attach basic Lambda execution policy
aws iam attach-role-policy \
  --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create custom policy for Bedrock and other services
aws iam create-policy \
  --policy-name workflow-optimization-policy \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "bedrock:InvokeModel"
        ],
        "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
      },
      {
        "Effect": "Allow",
        "Action": [
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": "arn:aws:s3:::workflow-optimization-data/*"
      },
      {
        "Effect": "Allow",
        "Action": [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ],
        "Resource": [
          "arn:aws:dynamodb:us-east-1:*:table/workflow-processing-state*",
          "arn:aws:dynamodb:us-east-1:*:table/agent-performance-metrics*",
          "arn:aws:dynamodb:us-east-1:*:table/workflow-optimization-results*",
          "arn:aws:dynamodb:us-east-1:*:table/system-configuration*"
        ]
      },
      {
        "Effect": "Allow",
        "Action": [
          "lambda:InvokeFunction"
        ],
        "Resource": "arn:aws:lambda:us-east-1:*:function:*-agent"
      }
    ]
  }'

# Attach custom policy to role
aws iam attach-role-policy \
  --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::ACCOUNT_ID:policy/workflow-optimization-policy
```

### 5. Deploy Lambda Functions

```bash
# Build and deploy using SAM
sam build

# Deploy with guided configuration
sam deploy --guided

# Or deploy with parameters
sam deploy \
  --stack-name workflow-optimization-system \
  --s3-bucket your-sam-deployment-bucket \
  --parameter-overrides \
    Environment=prod \
    S3Bucket=workflow-optimization-data \
    BedrockRegion=us-east-1 \
  --capabilities CAPABILITY_IAM
```

### 6. Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api \
  --name workflow-optimization-api \
  --description "Multi-agent workflow optimization system API" \
  --endpoint-configuration types=REGIONAL

# Get API ID
API_ID=$(aws apigateway get-rest-apis --query 'items[?name==`workflow-optimization-api`].id' --output text)

# Create resources and methods (simplified example)
# Note: Full API Gateway setup requires multiple commands
# Consider using SAM template or AWS CDK for complete deployment

# Deploy API
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod
```

## Post-Deployment Configuration

### 1. Initialize System Configuration

```bash
# Add default configuration values to DynamoDB
aws dynamodb put-item \
  --table-name system-configuration \
  --item '{
    "config_category": {"S": "thresholds"},
    "config_key": {"S": "max_processing_time"},
    "config_value": {"S": "300"},
    "data_type": {"S": "number"},
    "description": {"S": "Maximum processing time in seconds"},
    "environment": {"S": "prod"},
    "version": {"N": "1"}
  }'

aws dynamodb put-item \
  --table-name system-configuration \
  --item '{
    "config_category": {"S": "quality"},
    "config_key": {"S": "minimum_quality_score"},
    "config_value": {"S": "0.8"},
    "data_type": {"S": "number"},
    "description": {"S": "Minimum acceptable quality score"},
    "environment": {"S": "prod"},
    "version": {"N": "1"}
  }'
```

### 2. Test System Functionality

```bash
# Test input processing agent
aws lambda invoke \
  --function-name input-processing-agent \
  --payload '{
    "workflow_data": "Test approval process with 3 steps",
    "context": "University travel approval",
    "agent_role": "input"
  }' \
  response.json

# Check response
cat response.json

# Test orchestration agent with simple workflow
aws lambda invoke \
  --function-name orchestration-agent \
  --payload '{
    "action": "optimize",
    "workflow_data": {
      "description": "University faculty travel approval process",
      "steps": ["Submit request", "Manager approval", "Finance approval"],
      "cycle_time": 7,
      "rejection_rate": 0.15
    },
    "analysis_type": "comprehensive",
    "output_format": "executive_summary"
  }' \
  orchestration_response.json

cat orchestration_response.json
```

### 3. Validate Data Upload

```bash
# Verify training data upload
aws s3 ls s3://workflow-optimization-data/training_data/ --recursive

# Verify framework knowledge upload  
aws s3 ls s3://workflow-optimization-data/framework_knowledge/ --recursive

# Test framework knowledge loading
aws lambda invoke \
  --function-name analysis-agent \
  --payload '{
    "action": "test_framework_loading"
  }' \
  framework_test.json
```

## Monitoring and Logging

### 1. Set Up CloudWatch Alarms

```bash
# Create alarm for Lambda errors
aws cloudwatch put-metric-alarm \
  --alarm-name "workflow-optimization-lambda-errors" \
  --alarm-description "Lambda function errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2

# Create alarm for API Gateway 4XX errors
aws cloudwatch put-metric-alarm \
  --alarm-name "workflow-optimization-api-4xx" \
  --alarm-description "API Gateway 4XX errors" \
  --metric-name 4XXError \
  --namespace AWS/ApiGateway \
  --statistic Sum \
  --period 300 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2
```

### 2. Configure Log Retention

```bash
# Set log retention for Lambda functions
aws logs put-retention-policy \
  --log-group-name /aws/lambda/input-processing-agent \
  --retention-in-days 30

aws logs put-retention-policy \
  --log-group-name /aws/lambda/analysis-agent \
  --retention-in-days 30

aws logs put-retention-policy \
  --log-group-name /aws/lambda/optimization-agent \
  --retention-in-days 30

aws logs put-retention-policy \
  --log-group-name /aws/lambda/output-agent \
  --retention-in-days 30

aws logs put-retention-policy \
  --log-group-name /aws/lambda/orchestration-agent \
  --retention-in-days 90
```

## Validation and Testing

### 1. Run Validation Test Suite

```bash
# Execute validation tests using prepared test cases
python validation_scripts/run_validation_tests.py \
  --api-endpoint https://your-api-id.execute-api.us-east-1.amazonaws.com/prod \
  --test-cases validation_data/validation_cases.json \
  --output-file validation_results.json

# Run benchmark tests
python validation_scripts/run_benchmark_tests.py \
  --api-endpoint https://your-api-id.execute-api.us-east-1.amazonaws.com/prod \
  --benchmarks validation_data/benchmark_examples.json \
  --output-file benchmark_results.json
```

### 2. Performance Testing

```bash
# Load testing with university test data
python validation_scripts/performance_test.py \
  --api-endpoint https://your-api-id.execute-api.us-east-1.amazonaws.com/prod \
  --test-data validation_data/university_test_data.json \
  --concurrent-requests 10 \
  --duration 300
```

### 3. Academic Validation

```bash
# Validate against BPI Challenge benchmarks
python validation_scripts/academic_validation.py \
  --bpi-data s3://workflow-optimization-data/bpi_challenge_data/ \
  --framework-knowledge s3://workflow-optimization-data/framework_knowledge/ \
  --output-file academic_validation_results.json
```

## Troubleshooting

### Common Issues

1. **Bedrock Access Denied**
   - Verify model access is approved in Bedrock console
   - Check IAM permissions for bedrock:InvokeModel
   - Ensure correct model ID in Lambda environment variables

2. **Lambda Timeout Errors**
   - Increase timeout values in Lambda configuration
   - Check for infinite loops in processing logic
   - Monitor memory usage and increase if needed

3. **DynamoDB Throttling**
   - Check if tables are in on-demand billing mode
   - Review GSI usage and optimize queries
   - Consider increasing provisioned capacity if using provisioned mode

4. **S3 Access Issues**
   - Verify bucket permissions and IAM policies
   - Check bucket names in environment variables
   - Ensure proper S3 object keys in code

### Debug Commands

```bash
# Check Lambda function logs
aws logs describe-log-streams \
  --log-group-name /aws/lambda/orchestration-agent \
  --order-by LastEventTime \
  --descending

# Get recent log events
aws logs get-log-events \
  --log-group-name /aws/lambda/orchestration-agent \
  --log-stream-name LATEST_STREAM_NAME

# Check DynamoDB table status
aws dynamodb describe-table --table-name workflow-processing-state

# Monitor API Gateway usage
aws apigateway get-usage \
  --usage-plan-id YOUR_USAGE_PLAN_ID \
  --start-date 2024-01-01 \
  --end-date 2024-01-31
```

## Security Considerations

### 1. API Security
- Use API keys for all endpoints
- Implement IP whitelisting if needed
- Enable AWS WAF for additional protection
- Monitor for unusual API usage patterns

### 2. Data Security
- Ensure S3 bucket is not publicly accessible
- Use encrypted connections (HTTPS/TLS)
- Implement data retention policies
- Regular security audits

### 3. Access Control
- Follow principle of least privilege for IAM roles
- Use VPC endpoints for internal communication
- Implement proper logging and monitoring
- Regular access reviews

## Maintenance

### 1. Regular Updates
- Update Lambda runtime versions
- Refresh framework knowledge base
- Update training data with new examples
- Monitor for security patches

### 2. Performance Optimization
- Review CloudWatch metrics monthly
- Optimize Lambda memory allocations
- Clean up old DynamoDB records
- Monitor S3 storage costs

### 3. Backup and Recovery
- Enable point-in-time recovery for DynamoDB
- Implement S3 versioning and lifecycle policies
- Document restore procedures
- Test backup/restore processes quarterly

## Cost Management

### 1. Monitor Costs
- Set up billing alerts
- Review AWS Cost Explorer monthly
- Optimize resource usage based on patterns
- Consider Reserved Instances for predictable workloads

### 2. Optimization Strategies
- Use DynamoDB on-demand billing for variable workloads
- Implement S3 lifecycle policies
- Optimize Lambda memory and timeout settings
- Monitor Bedrock token usage

## Support and Documentation

### Additional Resources
- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- AWS Lambda Documentation: https://docs.aws.amazon.com/lambda/
- System API Documentation: `/documentation/api_documentation.json`
- Framework Knowledge Guide: `/framework_knowledge/README.md`

### Getting Help
- AWS Support (if you have a support plan)
- AWS Community Forums
- System logs and monitoring dashboards
- Academic supervisor or research team

## Next Steps

After successful deployment:

1. **Validate Research Requirements**
   - Confirm system meets dissertation requirements
   - Validate against academic benchmarks
   - Document performance metrics

2. **Conduct Research Experiments**
   - Run comparative studies vs. single-agent approaches
   - Measure improvement over baseline processes
   - Collect data for academic publication

3. **Scale and Optimize**
   - Monitor performance under realistic loads
   - Optimize based on usage patterns
   - Prepare for production use cases

4. **Academic Deliverables**
   - Generate research results and metrics
   - Prepare academic papers and presentations
   - Document lessons learned and future work