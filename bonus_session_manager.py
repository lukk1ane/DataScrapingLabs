import requests
from bs4 import BeautifulSoup
import json
import time
import threading
from datetime import datetime, timedelta
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class UserAccount:
    """Represents a user account"""
    username: str
    password: str
    session_id: Optional[str] = None
    last_login: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    login_attempts: int = 0
    is_active: bool = False
    csrf_token: Optional[str] = None

@dataclass
class SessionStatus:
    """Represents the status of a session"""
    user: str
    is_valid: bool
    last_check: datetime
    response_code: int
    error_message: Optional[str] = None

class SessionManager:
    """
    Advanced session manager for handling multiple user sessions
    Features:
    - Multiple account login
    - Session rotation
    - Session validation monitoring
    - Automatic re-authentication
    - Session health alerts
    """
    
    def __init__(self, base_url: str = "https://www.scrapingcourse.com"):
        self.base_url = base_url
        self.accounts: Dict[str, UserAccount] = {}
        self.sessions: Dict[str, requests.Session] = {}
        self.session_status: Dict[str, SessionStatus] = {}
        self.current_user_index = 0
        self.monitoring_active = False
        self.monitoring_thread = None
        self.rotation_interval = 30  # seconds
        self.health_check_interval = 60  # seconds
        
        # Statistics
        self.stats = {
            'total_logins': 0,
            'failed_logins': 0,
            'session_invalidations': 0,
            'successful_rotations': 0,
            'health_checks': 0
        }
    
    def add_account(self, username: str, password: str) -> None:
        """Add a user account to the manager"""
        self.accounts[username] = UserAccount(username=username, password=password)
        self.sessions[username] = requests.Session()
        logger.info(f"Added account: {username}")
    
    def login_account(self, username: str, use_csrf: bool = True) -> bool:
        """
        Login a specific account
        Returns True if login successful, False otherwise
        """
        if username not in self.accounts:
            logger.error(f"Account {username} not found")
            return False
        
        account = self.accounts[username]
        session = self.sessions[username]
        
        try:
            # Choose login URL based on CSRF requirement
            login_url = f"{self.base_url}/login/csrf" if use_csrf else f"{self.base_url}/login"
            
            logger.info(f"Logging in {username} to {login_url}")
            
            # Get login page
            response = session.get(login_url)
            if response.status_code != 200:
                logger.error(f"Failed to access login page for {username}: {response.status_code}")
                account.login_attempts += 1
                return False
            
            # Parse login form
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')
            
            if not form:
                logger.error(f"No login form found for {username}")
                account.login_attempts += 1
                return False
            
            # Extract form data
            action = form.get('action', '')
            method = form.get('method', 'post').lower()
            
            # Build login URL
            if action.startswith('/'):
                login_post_url = self.base_url + action
            elif action.startswith('http'):
                login_post_url = action
            else:
                login_post_url = login_url + '/' + action if action else login_url
            
            # Extract form fields
            form_data = {}
            csrf_token = None
            
            for input_field in form.find_all('input'):
                name = input_field.get('name')
                value = input_field.get('value', '')
                input_type = input_field.get('type', 'text')
                
                if name:
                    if input_type == 'hidden':
                        form_data[name] = value
                        if any(keyword in name.lower() for keyword in ['csrf', 'token', '_token', 'authenticity']):
                            csrf_token = value
                    elif name.lower() in ['username', 'email', 'user']:
                        form_data[name] = account.username
                    elif name.lower() in ['password', 'pass']:
                        form_data[name] = account.password
                    else:
                        form_data[name] = value
            
            # Store CSRF token
            account.csrf_token = csrf_token
            
            # Submit login
            if method == 'post':
                login_response = session.post(login_post_url, data=form_data)
            else:
                login_response = session.get(login_post_url, params=form_data)
            
            # Check login success
            if login_response.status_code in [200, 302] and "login" not in login_response.url.lower():
                account.is_active = True
                account.last_login = datetime.now()
                account.last_activity = datetime.now()
                account.login_attempts = 0
                
                # Extract session info
                for cookie in session.cookies:
                    if any(keyword in cookie.name.lower() for keyword in ['session', 'auth']):
                        account.session_id = cookie.value
                        break
                
                self.session_status[username] = SessionStatus(
                    user=username,
                    is_valid=True,
                    last_check=datetime.now(),
                    response_code=login_response.status_code
                )
                
                self.stats['total_logins'] += 1
                logger.info(f"Successfully logged in {username}")
                return True
            else:
                account.login_attempts += 1
                self.stats['failed_logins'] += 1
                logger.error(f"Login failed for {username}: {login_response.status_code}")
                return False
                
        except Exception as e:
            account.login_attempts += 1
            self.stats['failed_logins'] += 1
            logger.error(f"Exception during login for {username}: {e}")
            return False
    
    def login_all_accounts(self, use_csrf: bool = True) -> Dict[str, bool]:
        """Login all registered accounts"""
        results = {}
        
        for username in self.accounts.keys():
            results[username] = self.login_account(username, use_csrf)
            time.sleep(1)  # Small delay between logins
        
        active_sessions = sum(1 for result in results.values() if result)
        logger.info(f"Logged in {active_sessions}/{len(self.accounts)} accounts")
        
        return results
    
    def validate_session(self, username: str) -> bool:
        """
        Validate if a session is still active by accessing a protected page
        Returns True if session is valid, False otherwise
        """
        if username not in self.sessions:
            return False
        
        session = self.sessions[username]
        account = self.accounts[username]
        
        try:
            # Test access to protected products page
            products_url = f"{self.base_url}/dashboard"
            response = session.get(products_url, timeout=10)
            
            is_valid = response.status_code == 200 and "login" not in response.url.lower()
            
            # Update session status
            self.session_status[username] = SessionStatus(
                user=username,
                is_valid=is_valid,
                last_check=datetime.now(),
                response_code=response.status_code,
                error_message=None if is_valid else "Access denied or redirected to login"
            )
            
            if is_valid:
                account.last_activity = datetime.now()
            else:
                account.is_active = False
                logger.warning(f"Session invalidated for {username}")
                self.stats['session_invalidations'] += 1
            
            self.stats['health_checks'] += 1
            return is_valid
            
        except Exception as e:
            self.session_status[username] = SessionStatus(
                user=username,
                is_valid=False,
                last_check=datetime.now(),
                response_code=0,
                error_message=str(e)
            )
            account.is_active = False
            logger.error(f"Session validation failed for {username}: {e}")
            return False
    
    def get_next_active_session(self) -> Optional[str]:
        """Get the next active session for rotation"""
        active_users = [username for username, account in self.accounts.items() if account.is_active]
        
        if not active_users:
            return None
        
        # Round-robin selection
        if self.current_user_index >= len(active_users):
            self.current_user_index = 0
        
        selected_user = active_users[self.current_user_index]
        self.current_user_index += 1
        
        return selected_user
    
    def rotate_session(self) -> Optional[str]:
        """Rotate to the next available session"""
        next_user = self.get_next_active_session()
        
        if next_user:
            # Validate the session before using it
            if self.validate_session(next_user):
                self.stats['successful_rotations'] += 1
                logger.info(f"Rotated to session: {next_user}")
                return next_user
            else:
                # Try to re-login if session is invalid
                logger.info(f"Session invalid for {next_user}, attempting re-login")
                if self.login_account(next_user):
                    self.stats['successful_rotations'] += 1
                    return next_user
        
        logger.warning("No active sessions available for rotation")
        return None
    
    def monitor_sessions(self):
        """Background monitoring of all sessions"""
        while self.monitoring_active:
            try:
                logger.info("Starting session health check...")
                
                for username in self.accounts.keys():
                    if not self.monitoring_active:
                        break
                    
                    if self.accounts[username].is_active:
                        is_valid = self.validate_session(username)
                        
                        if not is_valid:
                            self.alert_session_invalid(username)
                            # Attempt automatic re-login
                            logger.info(f"Attempting automatic re-login for {username}")
                            self.login_account(username)
                    
                    time.sleep(2)  # Small delay between checks
                
                # Wait for next health check cycle
                time.sleep(self.health_check_interval)
                
            except Exception as e:
                logger.error(f"Error in session monitoring: {e}")
                time.sleep(30)  # Wait before retrying
    
    def alert_session_invalid(self, username: str):
        """Alert when a session becomes invalid"""
        logger.warning(f" ALERT: Session invalidated for user {username}")
        
        # Log detailed information
        status = self.session_status.get(username)
        if status:
            logger.warning(f"   Status Code: {status.response_code}")
            logger.warning(f"   Error: {status.error_message}")
            logger.warning(f"   Last Check: {status.last_check}")
    
    def start_monitoring(self):
        """Start background session monitoring"""
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self.monitor_sessions)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            logger.info("Session monitoring started")
    
    def stop_monitoring(self):
        """Stop background session monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("Session monitoring stopped")
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """
        Make a request using the current active session with automatic rotation
        """
        current_user = self.get_next_active_session()
        
        if not current_user:
            logger.error("No active sessions available for request")
            return None
        
        session = self.sessions[current_user]
        
        try:
            if method.upper() == 'GET':
                response = session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = session.post(url, **kwargs)
            else:
                response = session.request(method, url, **kwargs)
            
            # Update last activity
            self.accounts[current_user].last_activity = datetime.now()
            
            logger.info(f"Request to {url} using session {current_user}: {response.status_code}")
            return response
            
        except Exception as e:
            logger.error(f"Request failed using session {current_user}: {e}")
            return None
    
    def get_session_report(self) -> Dict:
        """Generate a comprehensive session report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_accounts': len(self.accounts),
            'active_sessions': sum(1 for account in self.accounts.values() if account.is_active),
            'statistics': self.stats,
            'accounts': {},
            'session_status': {}
        }
        
        # Account details
        for username, account in self.accounts.items():
            report['accounts'][username] = {
                'is_active': account.is_active,
                'last_login': account.last_login.isoformat() if account.last_login else None,
                'last_activity': account.last_activity.isoformat() if account.last_activity else None,
                'login_attempts': account.login_attempts,
                'session_id': account.session_id[:10] + "..." if account.session_id else None
            }
        
        # Session status
        for username, status in self.session_status.items():
            report['session_status'][username] = {
                'is_valid': status.is_valid,
                'last_check': status.last_check.isoformat(),
                'response_code': status.response_code,
                'error_message': status.error_message
            }
        
        return report
    
    def save_session_report(self, filename: str = 'session_report.json'):
        """Save session report to file"""
        report = self.get_session_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        logger.info(f"Session report saved to {filename}")

def demo_session_manager():
    """Demonstration of the SessionManager capabilities"""
    
    print("🚀 Starting Session Manager Demo")
    print("=" * 50)
    
    # Initialize session manager
    manager = SessionManager()
    
    # Add multiple demo accounts (using admin credentials for demo)
    accounts = [
        ('admin@example.com', 'password'),
        ('admin@example.com', 'password'),  # Using same credentials for demo
        ('admin@example.com', 'password'),
    ]
    
    for username, password in accounts:
        manager.add_account(username, password)
    
    print(f"Added {len(accounts)} accounts to session manager")
    
    # Login all accounts
    print("\n📝 Logging in all accounts...")
    login_results = manager.login_all_accounts(use_csrf=True)
    
    for username, success in login_results.items():
        status = " Success" if success else " Failed"
        print(f"  {username}: {status}")
    
    # Start session monitoring
    print("\n🔍 Starting session monitoring...")
    manager.start_monitoring()
    
    # Demonstrate session rotation
    print("\n🔄 Demonstrating session rotation...")
    for i in range(5):
        current_session = manager.rotate_session()
        if current_session:
            print(f"  Rotation {i+1}: Using session {current_session}")
            
            # Make a test request
            response = manager.make_request(f"{manager.base_url}/products")
            if response:
                print(f"    Request successful: {response.status_code}")
        else:
            print(f"  Rotation {i+1}: No active sessions available")
        
        time.sleep(3)
    
    # Session validation
    print("\n Validating all sessions...")
    for username in manager.accounts.keys():
        is_valid = manager.validate_session(username)
        status = "Valid" if is_valid else "Invalid"
        print(f"  {username}: {status}")
    
    # Generate and display report
    print("\n📊 Session Report:")
    report = manager.get_session_report()
    print(f"  Total Accounts: {report['total_accounts']}")
    print(f"  Active Sessions: {report['active_sessions']}")
    print(f"  Total Logins: {report['statistics']['total_logins']}")
    print(f"  Failed Logins: {report['statistics']['failed_logins']}")
    print(f"  Session Invalidations: {report['statistics']['session_invalidations']}")
    print(f"  Successful Rotations: {report['statistics']['successful_rotations']}")
    
    # Save detailed report
    manager.save_session_report()
    
    # Let it run for a bit to demonstrate monitoring
    print("\n  Running monitoring for 30 seconds...")
    time.sleep(30)
    
    # Stop monitoring
    manager.stop_monitoring()
    
    print("\n🏁 Session Manager Demo completed!")
    print("Check 'session_report.json' for detailed session information.")

if __name__ == "__main__":
    demo_session_manager() 