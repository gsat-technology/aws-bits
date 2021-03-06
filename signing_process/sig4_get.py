# AWS Version 4 signing example

# EC2 API (DescribeRegions)

# See: http://docs.aws.amazon.com/general/latest/gr/sigv4_signing.html
# This version makes a GET request and passes the signature
# in the Authorization header.
import sys, os, base64, datetime, hashlib, hmac, base64
import requests # pip install requests

# ************* REQUEST VALUES *************
method = 'GET'
service = 'ec2'
host = 'ec2.amazonaws.com'
region = 'us-east-1'
endpoint = 'https://ec2.amazonaws.com'
request_parameters = 'Action=DescribeRegions&Version=2013-10-15'

# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    r = [ hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest(), hmac.new(key, msg.encode('utf-8'), hashlib.sha256).hexdigest() ]
    return r

def getSignatureKey(key, dateStamp, regionName, serviceName):
    print("first create a 'signature key'")
    print('inputs to produce the signature key are these params:')
    print('\tsecret key:<aws secret key>\n\tdate stamp: {} \n\tregion: {}\n\tservice: {}'.format(dateStamp, regionName, serviceName))

    print('')
    kDate, kDateHex = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    print('\tdate stamp (signed with secret access key): {}...'.format(kDateHex[:20]))
    
    kRegion, kRegionHex = sign(kDate, regionName)
    print('\tregion (signed with signed date): {}...'.format(kRegionHex[:20]))

    kService, KServiceHex = sign(kRegion, serviceName)
    print('\tservice (signed with signed region): {}...'.format(KServiceHex[:20]))

    kSigning, kSigningHex = sign(kService, 'aws4_request')
    print('\tsigning key ("aws4_request" string signed with signed service): {}'.format(kSigningHex))
    
    return kSigning

# Read AWS access key from env. variables or configuration file. Best practice is NOT
# to embed credentials in code.
access_key = os.environ.get('AWS_ACCESS_KEY_ID')
secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
if access_key is None or secret_key is None:
    print 'No access key is available.'
    sys.exit()

# Create a date for headers and the credential string
t = datetime.datetime.utcnow()
amzdate = t.strftime('%Y%m%dT%H%M%SZ')
datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope


# ************* TASK 1: CREATE A CANONICAL REQUEST *************
# http://docs.aws.amazon.com/general/latest/gr/sigv4-create-canonical-request.html

# Step 1 is to define the verb (GET, POST, etc.)--already done.

# Step 2: Create canonical URI--the part of the URI from domain to query 
# string (use '/' if no path)
canonical_uri = '/' 

# Step 3: Create the canonical query string. In this example (a GET request),
# request parameters are in the query string. Query string values must
# be URL-encoded (space=%20). The parameters must be sorted by name.
# For this example, the query string is pre-formatted in the request_parameters variable.
canonical_querystring = request_parameters

# Step 4: Create the canonical headers and signed headers. Header names
# must be trimmed and lowercase, and sorted in code point order from
# low to high. Note that there is a trailing \n.
canonical_headers = 'host:' + host + '\n' + 'x-amz-date:' + amzdate + '\n'

# Step 5: Create the list of signed headers. This lists the headers
# in the canonical_headers list, delimited with ";" and in alpha order.
# Note: The request can include any headers; canonical_headers and
# signed_headers lists those that you want to be included in the 
# hash of the request. "Host" and "x-amz-date" are always required.
signed_headers = 'host;x-amz-date'

# Step 6: Create payload hash (hash of the request body content). For GET
# requests, the payload is an empty string ("").
payload_hash = hashlib.sha256('').hexdigest()
print('')
print('1. Create a payload hash')
print('for GET requests, the hash is created from empty string ("")')
print('____________')
print(payload_hash)
print('____________')
raw_input('')

# Step 7: Combine elements to create create canonical request
canonical_request = method + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

print('')
print("2. Create a canonical request")
print("i.e. a string representation of the HTTP request")
print("_________________")
print(canonical_request)
print("_________________")
raw_input('')

# ************* TASK 2: CREATE THE STRING TO SIGN*************
# Match the algorithm to the hashing algorithm you use, either SHA-1 or
# SHA-256 (recommended)
algorithm = 'AWS4-HMAC-SHA256'
credential_scope = datestamp + '/' + region + '/' + service + '/' + 'aws4_request'

string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()

print("3. Create a string to sign")
print("(i've annotated sections of the string below)")
print("_________________")
print('{}\t<-- algorithm'.format(algorithm))
print('{}\t<-- amzdate'.format(amzdate))
print('{}\t<-- credential_scope'.format(credential_scope))
print('{}\t<-- hash of canonical request'.format(hashlib.sha256(canonical_request).hexdigest()))
print("_________________")
raw_input('')

# ************* TASK 3: CALCULATE THE SIGNATURE *************
# Create the signing key using the function defined above.

print("3. Calculate the signature")

signing_key = getSignatureKey(secret_key, datestamp, region, service)

#print statements embedded in getSignatureKey() function
raw_input('')

# Sign the string_to_sign using the signing_key
signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

print('')
print("Sign the string with the signature key to create the signature")
print("_________________")
print('{}\t<-- signature'.format(signature))
print("_________________")

raw_input('')

# ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
# The signing information can be either in a query string value or in 
# a header named Authorization. This code shows how to use a header.
# Create authorization header and add to request headers
authorization_header = algorithm + ' ' + 'Credential=' + access_key + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature

print("4. Add signing information to the header:")
print("_________________")
print('{}\t<-- signature'.format(authorization_header))
print("_________________")

# The request can include any headers, but MUST include "host", "x-amz-date", 
# and (for this scenario) "Authorization". "host" and "x-amz-date" must
# be included in the canonical_headers and signed_headers, as noted
# earlier. Order here is not significant.
# Python note: The 'host' header is added automatically by the Python 'requests' library.
headers = {'x-amz-date':amzdate, 'Authorization':authorization_header}


# ************* SEND THE REQUEST *************
request_url = endpoint + '?' + canonical_querystring

raw_input('')

print("5. Send the request:")
print("_________________")
print('{}\t<-- request url'.format(request_url))
print("_________________")

r = requests.get(request_url, headers=headers)

print 'Response code: %d\n' % r.status_code
#print r.text

