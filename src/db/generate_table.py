import boto3

def generate_table():
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://db:8000',
                         region_name='example',                 # note that if you create a table using different region name and aws key
                         aws_access_key_id='example',           # you won't see this table on the admin app
                         aws_secret_access_key='example')

    ddb.create_table(
        TableName='Users',                # create table Users
        AttributeDefinitions=[
            {
                'AttributeName': 'email',     # In this case, I only specified uuid as partition key (there is no sort key)
                'AttributeType': 'S'        # with type string
            },
            {
                'AttributeName': 'type',  # sort key
                'AttributeType': 'S'         # string type
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'email',     # attribute uuid serves as partition key
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'type',  # attribute "type" serves as sort key
                'KeyType': 'RANGE'
            }
        ],
        ProvisionedThroughput={             # specying read and write capacity units
            'ReadCapacityUnits': 10,        # these two values really depend on the app's traffic
            'WriteCapacityUnits': 10
        }
    )

    ddb.create_table(
        TableName='TimeRule',                
        AttributeDefinitions=[
            {
                'AttributeName': 'type',    
                'AttributeType': 'S'       
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'type',     
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={            
            'ReadCapacityUnits': 10,        
            'WriteCapacityUnits': 10
        }
    )
    print('Successfully created table TimeRule')