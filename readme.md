# NBA Data Lake 🏀

A data pipeline that automatically collects NBA player data and creates a queryable data lake using AWS services (S3, Glue, and Athena).

## System Overview

This project creates a data lake that:
- Fetches NBA player data from SportsData.io
- Stores raw data in S3
- Creates a structured data catalog using AWS Glue
- Enables SQL querying through Amazon Athena

## Prerequisites

- AWS Account with appropriate permissions
- Python 3.x
- SportsData.io API key
- Required Python packages:
  ```
  boto3
  requests
  python-dotenv
  ```

## Setup

1. Clone this repository
2. Create a `.env` file with your credentials:
   ```
   SPORTS_DATA_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install boto3 requests python-dotenv
   ```

## AWS Resources Created

The script automatically sets up:
- S3 bucket (`nba-data-lake0333333`)
- Glue database (`nba_data_lake`)
- Glue table (`nba_players`)
- Athena configuration and output location

## Data Structure

The Glue table is configured with these columns:
- PlayerID (int)
- FirstName (string)
- LastName (string)
- Team (string)
- Position (string)

## Usage

1. Run the script:
   ```bash
   python nba_data_lake.py
   ```

2. The script will:
   - Create an S3 bucket
   - Fetch current NBA player data
   - Upload data to S3 in JSON format
   - Configure Athena database
   - Create Glue table for querying

3. Query your data using Athena:
   ```sql
   SELECT * FROM nba_data_lake.nba_players LIMIT 10;
   ```

## Class Structure

`NBADataLake` class handles:
- AWS service initialization
- Data fetching from SportsData.io
- S3 bucket creation and data upload
- Glue table configuration
- Athena setup

## Key Methods

- `fetch_nba_data()`: Gets player data from API
- `create_bucket()`: Sets up S3 storage
- `upload_data_to_s3()`: Stores JSON data
- `create_glue_table()`: Configures data structure
- `configure_athena()`: Sets up query capability

## Error Handling

The script includes error handling for:
- S3 bucket creation failures
- API request issues
- Data upload problems
- Glue/Athena configuration errors

## AWS Region

Currently configured for `us-east-1`. To change regions, modify the `region` variable in the class initialization.

## Cost Considerations

This project uses AWS services that may incur costs:
- S3 storage
- Glue table management
- Athena queries

Consider setting up AWS budget alerts.

## Future Enhancements

Potential improvements:
- Add data partitioning
- Implement data validation
- Add transformation layers
- Create automated updates
- Add data visualization

## Troubleshooting

Common issues:
1. **Bucket creation fails**: Check AWS permissions
2. **API errors**: Verify API key in .env
3. **Glue table issues**: Ensure JSON format matches schema

## Security Notes

- Use IAM roles with minimum required permissions
- Never commit .env file
- Consider encrypting S3 bucket
- Use VPC endpoints when possible

## Need Help?

Create an issue in the repository with:
- Error messages
- AWS region
- Python version
- Steps to reproduce

## License

MIT License - Use freely, maintain attribution
