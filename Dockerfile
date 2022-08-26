FROM nvcr.io/nvidia/pytorch:22.07-py3

RUN git clone https://github.com/andrewyguo/dope_training.git \
# Note, installing manually instead of using pip install -r requirements.txt because 
# the base PyTorch container already has some dependencies installed. Installing using 
# requirements.txt will cause circular dependency issues.
&& pip install --no-input tensorboardX \
&& pip install --no-input boto3 \
&& pip install --no-input albumentations \
&& pip install --no-input opencv_python==4.5.4.60 \
&& apt-get update \
&& export DEBIAN_FRONTEND=noninteractive \ 
&& apt-get install s3cmd -y \
&& apt-get install -y libgl1 

WORKDIR ~/dope_training

# Uncomment and fill in if using s3 
# RUN mkdir ~/.aws \
# && echo "[default]" >> ~/.aws/config \
# && echo "aws_access_key_id = <YOUR_USER_NAME>" >> ~/.aws/config \
# && echo "aws_secret_access_key = <YOUR_SECRET_KEY>" >> ~/.aws/config \
# # Setup config files for s3 authentication 
# && echo "[default]" >> ~/.s3cfg \
# && echo "use_https = True" >> ~/.s3cfg \
# && echo "access_key = <YOUR_USER_NAME>" >> ~/.s3cfg \
# && echo "secret_key = <YOUR_SECRET_KEY>" >> ~/.s3cfg \
# && echo "bucket_location = us-east-1" >> ~/.s3cfg \
# && echo "host_base = <YOUR_ENDPOINT>" >> ~/.s3cfg \
# && echo "host_bucket = bucket-name" >> ~/.s3cfg 
