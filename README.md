##AWS Bits

###s3-html-form-post

Based on this [AWS article](https://aws.amazon.com/articles/1434) about using an html form to POST a file to S3.

I created a small script to drop values into the html form (e.g. the form needs to be signed by the supplied secret key etc etc.)

```
./generate <AWS_ACCESS_KEY> <AWS_SECRET_ACCESS_KEY> <bucket_name > www/index.html
```

Run the index.html file locally.

####IAM

Note: this example is setup so that when IAM evaluates the key, it matches the name of the user `${aws:username}` to the S3 object key. So, the `policy_doc.json` file has the key 'starts-with' (and matching input param in form) set to 's3test'. You will need to make a user called 's3test' to be able to use the form (that's not compulsory - just how I set it up)

Requires an IAM user with policy:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::<bucket_name>/${aws:username}/*"
            ]
        }
    ]
}
```

This is interesting and could be useful in a scenario where someone needs to submit a file to you. It could be hooked up to an S3 event to notify you when the file has been uploaded or do some file validation etc.

### lambda_plotly

Does a call to [Plotly](https://plot.ly) to append a row to a grid.

The Plotly python package uses configuration files which are located at ~/.plotly. Lambda doesn't like to read/write this specific location and it doesn't look like the location is configurable. No matter; using the HTTP API instead of Python SDK is just as simple.

This lambda function wraps up _requests_ to do the http POST heavy lifting. It's deliberately simple and would be useful to call with an async invocation.

Sample event:

```
{
    "user": "gsat",
    "api-key": "<API KEY>",
    "grid": 81,
    "rows": [[99, 5], [5, 5], [5, 5]]
}
```

###signing process

####sig4_get.py

Python script from this [AWS page](http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html) which I've annotated with output so that it's easy to step though to understand how an HTTP request gets signed.
