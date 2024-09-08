from botocore.exceptions import ClientError
from boto3.resources.base import ServiceResource

class UserRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db          # db resource will be injected when this repository is created in the main.py

    def get_all(self):
        table = self.__db.Table('Users')  # referencing to table Users
        response = table.scan()             # scan all data
        return response.get('Items', [])    # return data

    def get_user_registry(self, email: str, type: str):
        try:
            table = self.__db.Table('Users')              # referencing to table Users
            response = table.get_item(Key={'email': email, "type": type})     # get user using uid (partition key)
            return response['Item']                         # return single data
        except KeyError as e:
            return None
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_or_replace_user_registry(self, user: dict):
        table = self.__db.Table('Users')      # referencing to table Users
        response = table.put_item(Item=user)  # create user
        return response                         # return response from dynamodb

   
class TimeRuleRepository:
    def __init__(self, db: ServiceResource) -> None:
        self.__db = db          

    def get_all(self):
        table = self.__db.Table('TimeRule')  
        response = table.scan()             
        return response.get('Items', [])    

    def get_time_rule(self, type: str):
        try:
            table = self.__db.Table('TimeRule')              
            response = table.get_item(Key={'type': type})     
            return response['Item']                         
        except ClientError as e:
            raise ValueError(e.response['Error']['Message'])

    def create_time_rule(self, time_rule: dict):
        table = self.__db.Table('TimeRule')      
        response = table.put_item(Item=time_rule)  
        return response                         

    def update_time_rule(self, time_rule: dict):
        table = self.__db.Table("TimeRule")
        response = table.update_item(
            Key={"type": time_rule.get("type")},
            UpdateExpression="SET #time = :time, #limit = :limit",
            ExpressionAttributeValues={
                ":time": time_rule.get("time"),
                ":limit": time_rule.get("limit"),
            },
            ExpressionAttributeNames={
                "#time": "time",
                "#limit": "limit",
            },
            ReturnValues="UPDATED_NEW",
        )
        return response


    def delete_time_rule(self, type: str):
        table = self.__db.Table('TimeRule')      
        response = table.delete_item(           
            Key={'type': type}
        )
        return response