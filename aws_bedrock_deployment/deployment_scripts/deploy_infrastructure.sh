#!/bin/bash

# Multi-Agent Workflow Optimization System - Infrastructure Deployment Script
# Author: Dissertation Research System
# Version: 1.0

set -e  # Exit on any error

# Configuration
AWS_REGION="us-east-1"
BUCKET_NAME="workflow-optimization-data"
STACK_NAME="workflow-optimization-system"
ENVIRONMENT="prod"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed. Please install AWS CLI v2."
        exit 1
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured. Please run 'aws configure'."
        exit 1
    fi
    
    # Check SAM CLI
    if ! command -v sam &> /dev/null; then
        warning "SAM CLI not found. Some deployment options may be limited."
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed."
        exit 1
    fi
    
    # Check Bedrock access
    log "Checking AWS Bedrock access..."
    if ! aws bedrock list-foundation-models --region $AWS_REGION &> /dev/null; then
        error "Cannot access AWS Bedrock. Please ensure you have permissions and model access."
        exit 1
    fi
    
    # Check for Claude 3.5 Sonnet access
    CLAUDE_MODEL="anthropic.claude-3-5-sonnet-20241022-v2:0"
    if ! aws bedrock list-foundation-models --region $AWS_REGION | grep -q "claude-3-5-sonnet"; then
        warning "Claude 3.5 Sonnet may not be available. Please check model access in Bedrock console."
    fi
    
    success "Prerequisites check completed."
}

# Create S3 bucket and configure
setup_s3_bucket() {
    log "Setting up S3 bucket: $BUCKET_NAME"
    
    # Check if bucket exists
    if aws s3 ls "s3://$BUCKET_NAME" 2>&1 | grep -q 'NoSuchBucket'; then
        log "Creating S3 bucket..."
        aws s3 mb "s3://$BUCKET_NAME" --region $AWS_REGION
        success "S3 bucket created: $BUCKET_NAME"
    else
        log "S3 bucket already exists: $BUCKET_NAME"
    fi
    
    # Enable versioning
    log "Enabling S3 bucket versioning..."
    aws s3api put-bucket-versioning \
        --bucket $BUCKET_NAME \
        --versioning-configuration Status=Enabled
    
    # Set up encryption
    log "Configuring S3 bucket encryption..."
    aws s3api put-bucket-encryption \
        --bucket $BUCKET_NAME \
        --server-side-encryption-configuration '{
            "Rules": [{
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                }
            }]
        }'
    
    # Block public access
    log "Blocking public access to S3 bucket..."
    aws s3api put-public-access-block \
        --bucket $BUCKET_NAME \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    
    success "S3 bucket configuration completed."
}

# Upload data to S3
upload_data_to_s3() {
    log "Uploading data to S3..."
    
    # Check if directories exist
    if [ ! -d "training_data" ]; then
        error "training_data directory not found. Please ensure you're in the correct directory."
        exit 1
    fi
    
    # Upload training data
    log "Uploading training data..."
    aws s3 cp training_data/ "s3://$BUCKET_NAME/training_data/" --recursive
    
    # Upload framework knowledge
    log "Uploading framework knowledge..."
    aws s3 cp framework_knowledge/ "s3://$BUCKET_NAME/framework_knowledge/" --recursive
    
    # Upload validation data
    log "Uploading validation data..."
    aws s3 cp validation_data/ "s3://$BUCKET_NAME/validation_data/" --recursive
    
    # Upload BPI Challenge data if available
    if [ -d "../data" ]; then
        log "Uploading BPI Challenge data..."
        aws s3 cp ../data/ "s3://$BUCKET_NAME/bpi_challenge_data/" --recursive
    else
        warning "BPI Challenge data directory not found. Skipping..."
    fi
    
    success "Data upload completed."
}

# Create DynamoDB tables
create_dynamodb_tables() {
    log "Creating DynamoDB tables..."
    
    # Function to check if table exists
    table_exists() {
        aws dynamodb describe-table --table-name $1 --region $AWS_REGION &> /dev/null
    }
    
    # Create workflow processing state table
    if ! table_exists "workflow-processing-state"; then
        log "Creating workflow-processing-state table..."
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
                'IndexName=workflow-id-index,KeySchema=[{AttributeName=workflow_id,KeyType=HASH},{AttributeName=timestamp,KeyType=RANGE}],Projection={ProjectionType=ALL},BillingMode=PAY_PER_REQUEST' \
                'IndexName=processing-stage-index,KeySchema=[{AttributeName=processing_stage,KeyType=HASH},{AttributeName=timestamp,KeyType=RANGE}],Projection={ProjectionType=KEYS_ONLY},BillingMode=PAY_PER_REQUEST' \
            --billing-mode PAY_PER_REQUEST \
            --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
            --region $AWS_REGION
    else
        log "workflow-processing-state table already exists."
    fi
    
    # Create agent performance metrics table
    if ! table_exists "agent-performance-metrics"; then
        log "Creating agent-performance-metrics table..."
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
                'IndexName=session-metrics-index,KeySchema=[{AttributeName=session_id,KeyType=HASH},{AttributeName=metric_timestamp,KeyType=RANGE}],Projection={ProjectionType=ALL},BillingMode=PAY_PER_REQUEST' \
                'IndexName=quality-score-index,KeySchema=[{AttributeName=agent_name,KeyType=HASH},{AttributeName=quality_score,KeyType=RANGE}],Projection={ProjectionType=INCLUDE,NonKeyAttributes=[session_id,metric_timestamp,execution_time_ms]},BillingMode=PAY_PER_REQUEST' \
            --billing-mode PAY_PER_REQUEST \
            --region $AWS_REGION
    else
        log "agent-performance-metrics table already exists."
    fi
    
    # Create workflow optimization results table
    if ! table_exists "workflow-optimization-results"; then
        log "Creating workflow-optimization-results table..."
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
                'IndexName=inefficiency-score-index,KeySchema=[{AttributeName=inefficiency_score,KeyType=HASH},{AttributeName=optimization_timestamp,KeyType=RANGE}],Projection={ProjectionType=INCLUDE,NonKeyAttributes=[workflow_id,optimization_potential,session_id]},BillingMode=PAY_PER_REQUEST' \
            --billing-mode PAY_PER_REQUEST \
            --region $AWS_REGION
    else
        log "workflow-optimization-results table already exists."
    fi
    
    # Create system configuration table
    if ! table_exists "system-configuration"; then
        log "Creating system-configuration table..."
        aws dynamodb create-table \
            --table-name system-configuration \
            --attribute-definitions \
                AttributeName=config_category,AttributeType=S \
                AttributeName=config_key,AttributeType=S \
            --key-schema \
                AttributeName=config_category,KeyType=HASH \
                AttributeName=config_key,KeyType=RANGE \
            --billing-mode PAY_PER_REQUEST \
            --region $AWS_REGION
    else
        log "system-configuration table already exists."
    fi
    
    # Wait for tables to be active
    log "Waiting for tables to become active..."
    aws dynamodb wait table-exists --table-name workflow-processing-state --region $AWS_REGION
    aws dynamodb wait table-exists --table-name agent-performance-metrics --region $AWS_REGION
    aws dynamodb wait table-exists --table-name workflow-optimization-results --region $AWS_REGION
    aws dynamodb wait table-exists --table-name system-configuration --region $AWS_REGION
    
    success "DynamoDB tables created successfully."
}

# Create IAM roles and policies
create_iam_resources() {
    log "Creating IAM roles and policies..."
    
    # Check if role exists
    if ! aws iam get-role --role-name lambda-execution-role &> /dev/null; then
        log "Creating Lambda execution role..."
        aws iam create-role \
            --role-name lambda-execution-role \
            --assume-role-policy-document '{
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Principal": {"Service": "lambda.amazonaws.com"},
                    "Action": "sts:AssumeRole"
                }]
            }' > /dev/null
        
        # Attach basic Lambda execution policy
        aws iam attach-role-policy \
            --role-name lambda-execution-role \
            --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
    else
        log "Lambda execution role already exists."
    fi
    
    # Get account ID for policy ARN
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    
    # Check if custom policy exists
    if ! aws iam get-policy --policy-arn "arn:aws:iam::$ACCOUNT_ID:policy/workflow-optimization-policy" &> /dev/null; then
        log "Creating custom IAM policy..."
        aws iam create-policy \
            --policy-name workflow-optimization-policy \
            --policy-document '{
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["bedrock:InvokeModel"],
                        "Resource": "arn:aws:bedrock:'$AWS_REGION'::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["s3:GetObject", "s3:PutObject"],
                        "Resource": "arn:aws:s3:::'$BUCKET_NAME'/*"
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
                            "arn:aws:dynamodb:'$AWS_REGION':'$ACCOUNT_ID':table/workflow-processing-state*",
                            "arn:aws:dynamodb:'$AWS_REGION':'$ACCOUNT_ID':table/agent-performance-metrics*",
                            "arn:aws:dynamodb:'$AWS_REGION':'$ACCOUNT_ID':table/workflow-optimization-results*",
                            "arn:aws:dynamodb:'$AWS_REGION':'$ACCOUNT_ID':table/system-configuration*"
                        ]
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["lambda:InvokeFunction"],
                        "Resource": "arn:aws:lambda:'$AWS_REGION':'$ACCOUNT_ID':function:*-agent"
                    }
                ]
            }' > /dev/null
        
        # Attach custom policy to role
        aws iam attach-role-policy \
            --role-name lambda-execution-role \
            --policy-arn "arn:aws:iam::$ACCOUNT_ID:policy/workflow-optimization-policy"
    else
        log "Custom IAM policy already exists."
    fi
    
    success "IAM resources created successfully."
}

# Initialize system configuration
initialize_system_config() {
    log "Initializing system configuration..."
    
    # Add default configuration values
    aws dynamodb put-item \
        --table-name system-configuration \
        --item '{
            "config_category": {"S": "thresholds"},
            "config_key": {"S": "max_processing_time"},
            "config_value": {"S": "300"},
            "data_type": {"S": "number"},
            "description": {"S": "Maximum processing time in seconds"},
            "environment": {"S": "'$ENVIRONMENT'"},
            "version": {"N": "1"},
            "last_updated": {"N": "'$(date +%s)'"},
            "updated_by": {"S": "deployment_script"}
        }' \
        --region $AWS_REGION > /dev/null
    
    aws dynamodb put-item \
        --table-name system-configuration \
        --item '{
            "config_category": {"S": "quality"},
            "config_key": {"S": "minimum_quality_score"},
            "config_value": {"S": "0.8"},
            "data_type": {"S": "number"},
            "description": {"S": "Minimum acceptable quality score"},
            "environment": {"S": "'$ENVIRONMENT'"},
            "version": {"N": "1"},
            "last_updated": {"N": "'$(date +%s)'"},
            "updated_by": {"S": "deployment_script"}
        }' \
        --region $AWS_REGION > /dev/null
    
    aws dynamodb put-item \
        --table-name system-configuration \
        --item '{
            "config_category": {"S": "features"},
            "config_key": {"S": "multi_agent_enabled"},
            "config_value": {"S": "true"},
            "data_type": {"S": "boolean"},
            "description": {"S": "Enable multi-agent processing"},
            "environment": {"S": "'$ENVIRONMENT'"},
            "version": {"N": "1"},
            "last_updated": {"N": "'$(date +%s)'"},
            "updated_by": {"S": "deployment_script"}
        }' \
        --region $AWS_REGION > /dev/null
    
    aws dynamodb put-item \
        --table-name system-configuration \
        --item '{
            "config_category": {"S": "bedrock"},
            "config_key": {"S": "model_id"},
            "config_value": {"S": "anthropic.claude-3-5-sonnet-20241022-v2:0"},
            "data_type": {"S": "string"},
            "description": {"S": "Bedrock model identifier"},
            "environment": {"S": "'$ENVIRONMENT'"},
            "version": {"N": "1"},
            "last_updated": {"N": "'$(date +%s)'"},
            "updated_by": {"S": "deployment_script"}
        }' \
        --region $AWS_REGION > /dev/null
    
    success "System configuration initialized."
}

# Validate deployment
validate_deployment() {
    log "Validating deployment..."
    
    # Check S3 bucket access
    log "Validating S3 bucket access..."
    if aws s3 ls "s3://$BUCKET_NAME/training_data/" > /dev/null; then
        success "S3 bucket access validated."
    else
        error "S3 bucket validation failed."
        return 1
    fi
    
    # Check DynamoDB tables
    log "Validating DynamoDB tables..."
    tables=("workflow-processing-state" "agent-performance-metrics" "workflow-optimization-results" "system-configuration")
    for table in "${tables[@]}"; do
        if aws dynamodb describe-table --table-name $table --region $AWS_REGION > /dev/null; then
            log "Table $table is active."
        else
            error "Table $table validation failed."
            return 1
        fi
    done
    success "DynamoDB tables validated."
    
    # Check IAM role
    log "Validating IAM role..."
    if aws iam get-role --role-name lambda-execution-role > /dev/null; then
        success "IAM role validated."
    else
        error "IAM role validation failed."
        return 1
    fi
    
    success "Deployment validation completed successfully."
}

# Main deployment function
main() {
    log "Starting Multi-Agent Workflow Optimization System deployment..."
    log "Target AWS Region: $AWS_REGION"
    log "S3 Bucket: $BUCKET_NAME"
    log "Environment: $ENVIRONMENT"
    
    # Run deployment steps
    check_prerequisites
    setup_s3_bucket
    upload_data_to_s3
    create_dynamodb_tables
    create_iam_resources
    initialize_system_config
    validate_deployment
    
    success "Infrastructure deployment completed successfully!"
    
    log "Next steps:"
    log "1. Deploy Lambda functions using SAM CLI or manual deployment"
    log "2. Create API Gateway endpoints"
    log "3. Run validation tests"
    log "4. Configure monitoring and alerts"
    
    log "Deployment summary:"
    log "- S3 Bucket: s3://$BUCKET_NAME"
    log "- DynamoDB Tables: workflow-processing-state, agent-performance-metrics, workflow-optimization-results, system-configuration"
    log "- IAM Role: lambda-execution-role"
    log "- Region: $AWS_REGION"
}

# Handle script interruption
trap 'error "Deployment interrupted. Some resources may have been partially created."; exit 1' INT TERM

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --region)
            AWS_REGION="$2"
            shift 2
            ;;
        --bucket)
            BUCKET_NAME="$2"
            shift 2
            ;;
        --environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [--region REGION] [--bucket BUCKET_NAME] [--environment ENV]"
            echo "  --region      AWS region (default: us-east-1)"
            echo "  --bucket      S3 bucket name (default: workflow-optimization-data)"
            echo "  --environment Environment name (default: prod)"
            exit 0
            ;;
        *)
            error "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Execute main function
main