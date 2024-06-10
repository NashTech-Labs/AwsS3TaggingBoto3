import boto3

def update_bucket_name_tags():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
   
    for bucket in buckets:
        bucket_name = bucket['Name']
       
        # Retrieve existing tags for the bucket
        try:
            existing_tags = s3.get_bucket_tagging(Bucket=bucket_name)
            tag_set = existing_tags['TagSet']
        except s3.exceptions.ClientError as e:
            # If the bucket has no tags, set an empty tag set
            if e.response['Error']['Code'] == 'NoSuchTagSet':
                print(f"Bucket {bucket_name} has no tags, adding 'Name' tag...")
                tag_set = []
            else:
                raise
       
        # Check if the bucket already has a "Name" tag
        existing_name_tag = next((tag for tag in tag_set if tag['Key'] == 'Name'), None)
       
        # If the bucket does not have a "Name" tag, add it
        if not existing_name_tag:
            tag_set.append({'Key': 'Name', 'Value': bucket_name})
            response = s3.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={'TagSet': tag_set}
            )
            print(f"Name tag added for bucket: {bucket_name}")

def lambda_handler(event, context):
    update_bucket_name_tags()
    return {
        'statusCode': 200,
        'body': 'Name tags updated for all S3 buckets'
    }


