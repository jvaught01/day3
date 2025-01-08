import boto3
import json
import time
import requests
import dotenv
import os


dotenv.load_dotenv()

class NBADataLake:
    def __init__(self):
        self.region = "us-east-1"
        self.key = os.getenv("SPORTS_DATA_API_KEY")
        self.bucket_name = "nba-data-lake0333333"
        self.bucket = boto3.resource("s3").Bucket(self.bucket_name)
        self.glue_database_name = "nba_data_lake"
        self.athena_output_location = f"s3://{self.bucket_name}/athena_output"
        self.s3_client = boto3.client("s3", region_name=self.region)
        self.glue_client = boto3.client("glue", region_name=self.region)
        self.athena_client = boto3.client("athena", region_name=self.region)

    def fetch_nba_data(self):
        response = requests.get(f"https://api.sportsdata.io/v3/nba/scores/json/Players?key={self.key}")
        data = response.json()
        return data
    
    def create_bucket(self):
        try:
            self.s3_client.create_bucket(Bucket=self.bucket_name)
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def upload_data_to_s3(self, data, file_name):
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=file_name, Body=json.dumps(data))
        except Exception as e:
            print(f"Error uploading to S3: {e}")
            
    def create_glue_table(self):
        try:
            self.glue_client.create_table(
                DatabaseName=self.glue_database_name,
                            TableInput={
                "Name": "nba_players",
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "PlayerID", "Type": "int"},
                        {"Name": "FirstName", "Type": "string"},
                        {"Name": "LastName", "Type": "string"},
                        {"Name": "Team", "Type": "string"},
                        {"Name": "Position", "Type": "string"},
                    ],
                    "Location": f"s3://{self.bucket_name}/raw-data/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe"
                    },
                },
                "TableType": "EXTERNAL_TABLE",
            },
            )
            print(f"Glue table 'nba_players' created successfully.")
        except Exception as e:
            print(f"Error creating Glue table: {e}")

    def configure_athena(self):
        try:
            self.athena_client.start_query_execution(
                QueryString=f"CREATE DATABASE IF NOT EXISTS {self.glue_database_name}",
                QueryExecutionContext={"Database": self.glue_database_name},
                ResultConfiguration={"OutputLocation": self.athena_output_location}
            )
            print(f"Athena database '{self.glue_database_name}' created successfully.")
        except Exception as e:
            print(f"Error creating Athena database: {e}")


def main():
    nba_data_lake = NBADataLake()
    print("Creating bucket...")
    nba_data_lake.create_bucket()
    print("Fetching NBA data and uploading to S3...")
    nba_data_lake.upload_data_to_s3(nba_data_lake.fetch_nba_data(), "nba_players.json")
    print("Configuring Athena...")
    nba_data_lake.configure_athena()
    print("Creating Glue table...")
    nba_data_lake.create_glue_table()
    print("Setup completed successfully.")
if __name__ == "__main__":
    main()