#!/usr/bin bash

#aws iot describe-endpoint
export DEPLOYMENT_BUCKET=mangdang2023

##### no need to change anything below
export DANCE_FILE=demo.py
cd ~/environment/mini-pupper-aws
aws s3 cp greengrass/docker-compose.yaml s3://${DEPLOYMENT_BUCKET}/com.example.ros.pupper.dance/1.0.0/artifacts/docker-compose.yaml
aws greengrassv2 create-component-version     --inline-recipe fileb://greengrass/com.example.ros.pupper.dance/1.0.0/recipes/recipe.yaml
