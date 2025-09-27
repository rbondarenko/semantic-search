#!/bin/sh
# Verify ALB is internet-facing
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[].[LoadBalancerName,Scheme,State.Code]' \
  --output table

# Get ALB DNS name for external access
aws elbv2 describe-load-balancers \
  --query 'LoadBalancers[].DNSName' \
  --output text
