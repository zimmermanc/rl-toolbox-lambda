Lambda Setup Short Documentation

Supplied Files

lambda.zip



Create new S3 bucket for Report delivery. This bucket needs write access by lambda or specifically the lambda script we create.

Create new lambda function using lambda.zip

Variables ENV Variables required for lambda function below:

TargetS3Bucket    (Destination for log delivery)

Customername  ( Tenatn in Prisma/Redlock )

Username  (login for Prisma/Redlock)

Password  (password for Prisma/Redlock)

Url    ( api2.redlock.io )



Create Cloudwatch rule to execute lambda script as often as Wyndham would like this script run.
