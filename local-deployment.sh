APP_NAME="food-tracker-lambda"
CODE_BUCKET="dphilpott-dev-code-bucket"
ENV='prod'

echo "Deploying $APP_NAME to dev"

echo "Building Python dependencies in Lambda Docker image..."
mkdir -p temp/build/
docker build -t="pydeplmb" . && echo "Python dependencies built successfully!" || echo "Python dependency building failed"
docker run -dt pydeplmb
CONTAINER_ID=$(docker ps -alq) && echo "Now running container $CONTAINER_ID"
docker cp $CONTAINER_ID:/python/ temp/build/ && echo "Python dependencies retrieved!" || echo "Python dependency retrieval failed"
docker kill $CONTAINER_ID && echo "Killed container $CONTAINER_ID"
docker image rm -f pydeplmb

echo "Copying app files to build directory..."
cp -R app/ temp/build/python/app

echo "Packaging build..."
cd temp/build/python
chmod -R 777 ./*
zip -r ../../../$APP_NAME.zip .
cd ../../.. || exit
echo "Packaging complete!"

echo "Testing..."
if pytest -vv ; then
    echo "Test succeeded"
    echo "Uploading archive to S3..."
    aws s3 cp $APP_NAME.zip s3://$CODE_BUCKET/$APP_NAME/$ENV/$APP_NAME.zip  && echo "Artifact upload successful!" || echo "Artifact upload failed"
    echo "Removing build directory..."
    rm -rf temp/
    echo "Removing packaged build..."
    rm -rf $APP_NAME.zip
    echo "Running Terraform..."
    cd terraform
    terraform init --backend-config=environments/$ENV/backend.tfvars
    terraform apply -auto-approve --var-file=environments/$ENV/variables.tfvars

    echo "Updating Lambda..."
    aws lambda update-function-code \
    --function-name $APP_NAME-$ENV  \
    --s3-bucket $CODE_BUCKET \
    --s3-key $APP_NAME/$ENV/$APP_NAME.zip --no-publish
else
    echo "Test failed. Retaining build / package."
fi
