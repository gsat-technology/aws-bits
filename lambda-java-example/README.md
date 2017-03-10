
### Basic Java Lambda Deployment Package

- Uses maven
- Predefined Java interfaces from the `aws-lambda-java-core` library

###Package
```
cd lamda-java-example
mvn package
```

####Deploy

```
aws lambda create-function \
  --function-name basic-java-lambda \
  --zip-file fileb://target/lambda-java-example-1.0-SNAPSHOT.jar \
--role arn:aws:iam::{accountID}:role/lambda_basic_execution  \
--handler Hello \
--runtime java8 \
--timeout 15 \
--memory-size 512
```

####Test

test using event e.g.

````
{
  "firstName": "<first_name>",
  "lastName": "<last_name>"
}
```


#### Resources

Created based on these Resources:

[Creating a .jar Deployment Package Using Maven without any IDE (Java)](http://docs.aws.amazon.com/lambda/latest/dg/java-create-jar-pkg-maven-no-ide.html)

- project layout/pom configuration

[Leveraging Predefined Interfaces for Creating Handler (Java)](http://docs.aws.amazon.com/lambda/latest/dg/java-handler-using-predefined-interfaces.html)

- lambda function code
