import requests
import ssl
import socket
import datetime
import OpenSSL.crypto as crypto


def check_ssl_certificate():
    url = "https://www.python.org/"

    print("=== SSL Certificate Verification ===")

    try:
        response = requests.get(url)
        print(f"Request with SSL verification: Success (Status code: {response.status_code})")
    except requests.exceptions.SSLError as e:
        print(f"SSL Verification failed: {e}")

    try:
        response_no_verify = requests.get(url, verify=False)
        print(f"Request without SSL verification: Success (Status code: {response_no_verify.status_code})")
        print("WARNING: Disabling SSL verification is not secure!")
    except requests.exceptions.RequestException as e:
        print(f"Request failed even with SSL verification disabled: {e}")

    print("\n=== Certificate Information ===")
    try:
        hostname = url.split("//")[1].split("/")[0]

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_binary = ssock.getpeercert(binary_form=True)
                cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_binary)

                issuer = dict(cert.get_issuer().get_components())
                subject = dict(cert.get_subject().get_components())

                issuer = {k.decode(): v.decode() for k, v in issuer.items()}
                subject = {k.decode(): v.decode() for k, v in subject.items()}

                not_before = datetime.datetime.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ")
                not_after = datetime.datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")

                print(f"Domain: {hostname}")
                print(f"Issuer: {issuer.get('CN', 'Unknown')}")
                print(f"Organization: {subject.get('O', 'Unknown')}")
                print(f"Valid from: {not_before}")
                print(f"Valid until: {not_after}")
                print(f"Serial Number: {cert.get_serial_number()}")
                print(f"Version: {cert.get_version() + 1}")  # Version is 0-indexed

    except Exception as e:
        print(f"Failed to retrieve certificate information: {e}")


if __name__ == "__main__":
    check_ssl_certificate()