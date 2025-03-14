import requests
import ssl
import socket
import datetime
import certifi
import OpenSSL.crypto as crypto

def verify_ssl(url):
  
    if url.startswith("http://"):
        print(f"Warning: {url} is using HTTP, not HTTPS. SSL certificates are only used with HTTPS.")
        url = url.replace("http://", "https://")
        print(f"Attempting to connect using HTTPS instead: {url}")
    
    if not url.startswith("https://"):
        url = "https://" + url
    
    hostname = url.split("https://")[1].split("/")[0]
    
    print(f"Checking SSL certificate for: {hostname}\n")
    
    print("=== Standard SSL Verification ===")
    try:
        response = requests.get(url, timeout=10)
        print(f"✓ SSL verification successful")
        print(f"Status code: {response.status_code}")
    except requests.exceptions.SSLError as e:
        print(f"✗ SSL verification failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
    print()
    
    print("=== SSL Verification Disabled (INSECURE) ===")
    try:
        response = requests.get(url, verify=False, timeout=10)
        print(f"Request completed without verification (Status: {response.status_code})")
        print("WARNING: Disabling SSL verification is insecure and should only be used for testing!")
    except requests.exceptions.RequestException as e:
        print(f"Request failed even with verification disabled: {e}")
    print()
    
   
    print("=== Certificate Information ===")
    try:
       
        context = ssl.create_default_context(cafile=certifi.where())
    
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
               
                cert_binary = ssock.getpeercert(binary_form=True)
                cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_binary)
            
                subject = cert.get_subject()
                issuer = cert.get_issuer()
                
                
                not_before = datetime.datetime.strptime(cert.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
                not_after = datetime.datetime.strptime(cert.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
                
            
                print(f"Subject: {subject.CN}")
                print(f"Issuer: {issuer.CN}")
                print(f"Valid from: {not_before}")
                print(f"Valid until: {not_after}")
                
                now = datetime.datetime.utcnow()
                if now < not_after:
                    days_left = (not_after - now).days
                    print(f"Certificate is valid (expires in {days_left} days)")
                else:
                    print(f"Certificate has EXPIRED!")
                
                alt_names = []
                for i in range(cert.get_extension_count()):
                    ext = cert.get_extension(i)
                    if ext.get_short_name() == b'subjectAltName':
                        alt_names = str(ext).split(', ')
                
                if alt_names:
                    print("Alternative names:")
                    for name in alt_names:
                        print(f"  - {name}")
                
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except socket.error as e:
        print(f"Socket Error: {e}")
    except Exception as e:
        print(f"Error retrieving certificate information: {e}")

def main():
    url = "https://www.python.org"
    verify_ssl(url)
    
    print("\n" + "="*50 + "\n")
    url = "http://books.toscrape.com"
    verify_ssl(url)

if __name__ == "__main__":
    main()