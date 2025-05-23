#!/usr/bin/env python3
"""
LAB8 Bonus: Multi-Session Manager
Simulate managing and monitoring multiple user sessions with rotation,
validation tracking, and invalidation alerts.
"""

import requests
from bs4 import BeautifulSoup
import pickle
import json
import time
import threading
from datetime import datetime, timedelta
from urllib.parse import urljoin
import os
import random
from typing import Dict, List, Optional, Tuple


class UserSession:
    """Represents a user session with authentication and monitoring capabilities."""
    
    def __init__(self, email: str, password: str, session_id: str = None):
        self.email = email
        self.password = password
        self.session_id = session_id or f"session_{email.split('@')[0]}_{int(time.time())}"
        self.session = requests.Session()
        self.is_authenticated = False
        self.last_validated = None
        self.login_time = None
        self.last_activity = None
        self.validation_failures = 0
        self.cookies_backup = None
        
        # Set user agent
        self.session.headers.update({
            'User-Agent': f'SessionManager/{email} Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def __str__(self):
        status = "✅ Active" if self.is_authenticated else "❌ Inactive"
        return f"Session[{self.email}]: {status} (Last: {self.last_activity})"


class SessionManager:
    """Manages multiple user sessions with rotation and monitoring."""
    
    def __init__(self, login_url: str, protected_url: str, check_interval: int = 30):
        self.login_url = login_url
        self.protected_url = protected_url
        self.check_interval = check_interval
        self.sessions: Dict[str, UserSession] = {}
        self.current_session_id = None
        self.monitoring_active = False
        self.monitor_thread = None
        self.rotation_index = 0
        self.alerts = []
        
    def add_user(self, email: str, password: str) -> str:
        """Add a new user session to the manager."""
        session = UserSession(email, password)
        self.sessions[session.session_id] = session
        print(f"✅ Added user session: {email} (ID: {session.session_id})")
        return session.session_id
    
    def get_demo_credentials(self, session: requests.Session) -> Tuple[str, str]:
        """Extract or determine demo credentials from the login page."""
        try:
            response = session.get(self.login_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for demo credentials
            demo_info = soup.find('div', class_='alert') or \
                       soup.find('div', class_='demo-credentials') or \
                       soup.find('div', class_='challenge-info')
            
            if demo_info:
                text = demo_info.get_text().lower()
                print(f"Found credentials info: {text}")
                
                # Try to extract actual credentials from text
                if 'email' in text and 'password' in text:
                    # Common email patterns to try
                    common_emails = [
                        'admin@example.com',
                    ]
                    
                    # Try to find password in text
                    password = 'password'  # Default from the demo info
                    if 'password:' in text:
                        password_part = text.split('password:')[1].split()[0].strip()
                        if password_part and len(password_part) > 2:
                            password = password_part
                    
                    return common_emails[0], password  # Return first email to try
            
            # Default fallback credentials
            return 'admin@admin.com', 'password'
            
        except Exception as e:
            print(f"Error getting demo credentials: {e}")
            return 'admin@admin.com', 'password'
    
    def extract_csrf_token(self, session: requests.Session) -> Tuple[Optional[str], Optional[str]]:
        """Extract CSRF token from login page."""
        try:
            response = session.get(self.login_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            csrf_selectors = [
                'input[name="_token"]',
                'input[name="csrf_token"]',
                'input[name="authenticity_token"]',
                'meta[name="csrf-token"]',
                'meta[name="_token"]'
            ]
            
            for selector in csrf_selectors:
                csrf_element = soup.select_one(selector)
                if csrf_element:
                    token = csrf_element.get('value') or csrf_element.get('content')
                    if token:
                        field_name = csrf_element.get('name', 'csrf_token')
                        return token, field_name
            
            return None, None
        except Exception as e:
            print(f"❌ Error extracting CSRF token: {e}")
            return None, None
    
    def try_login_with_credentials(self, user_session: UserSession, email: str, password: str) -> bool:
        """Try logging in with specific credentials."""
        try:
            # Get login page and extract form data
            response = user_session.session.get(self.login_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            form = soup.find('form')
            
            if not form:
                return False
            
            # Extract form details
            action = form.get('action', '')
            form_url = urljoin(self.login_url, action) if action else self.login_url
            
            # Get CSRF token
            csrf_token, csrf_field_name = self.extract_csrf_token(user_session.session)
            
            # Find field names
            email_field = 'email'
            password_field = 'password'
            
            for input_field in form.find_all('input'):
                input_type = input_field.get('type', '').lower()
                input_name = input_field.get('name', '')
                
                if input_type in ['text', 'email'] or 'email' in input_name.lower():
                    email_field = input_name
                elif input_type == 'password':
                    password_field = input_name
            
            # Prepare login data
            login_data = {
                email_field: email,
                password_field: password
            }
            
            if csrf_token and csrf_field_name:
                login_data[csrf_field_name] = csrf_token
            
            # Add hidden fields
            for hidden_input in form.find_all('input', type='hidden'):
                name = hidden_input.get('name')
                value = hidden_input.get('value', '')
                if name and name != csrf_field_name:
                    login_data[name] = value
            
            # Submit login
            response = user_session.session.post(form_url, data=login_data, allow_redirects=True)
            response.raise_for_status()
            
            # Check if login was successful
            if 'login' in response.url.lower():
                soup = BeautifulSoup(response.content, 'html.parser')
                if soup.find('form'):
                    return False  # Still on login page
            
            # Update credentials if successful
            user_session.email = email
            user_session.password = password
            return True
            
        except Exception as e:
            print(f"❌ Login attempt error: {e}")
            return False
    
    def login_user(self, session_id: str) -> bool:
        """Login a specific user session with credential fallback."""
        if session_id not in self.sessions:
            print(f"❌ Session {session_id} not found")
            return False
        
        user_session = self.sessions[session_id]
        
        print(f"🔐 Logging in user: {user_session.email}")
        
        # Get actual demo credentials from the page
        demo_email, demo_password = self.get_demo_credentials(user_session.session)
        
        # Try multiple credential combinations
        credential_combinations = [
            (demo_email, demo_password),  # From page
            (user_session.email, user_session.password),  # Original
            ('admin@example.com', 'password'),  # Common pattern 1
        ]
        
        for email, password in credential_combinations:
            print(f"   Trying credentials: {email} / {password}")
            
            if self.try_login_with_credentials(user_session, email, password):
                # Update session state
                user_session.is_authenticated = True
                user_session.login_time = datetime.now()
                user_session.last_validated = datetime.now()
                user_session.last_activity = datetime.now()
                user_session.validation_failures = 0
                
                # Backup cookies
                user_session.cookies_backup = user_session.session.cookies.copy()
                
                print(f"✅ Login successful for {user_session.email} with {email}")
                return True
            else:
                print(f"   ❌ Failed with {email}")
        
        print(f"❌ All login attempts failed for {user_session.email}")
        return False
    
    def validate_session(self, session_id: str) -> bool:
        """Validate if a session is still active by accessing protected page."""
        if session_id not in self.sessions:
            return False
        
        user_session = self.sessions[session_id]
        
        if not user_session.is_authenticated:
            return False
        
        try:
            # Access protected page
            response = user_session.session.get(self.protected_url, timeout=10)
            
            # Update last activity
            user_session.last_activity = datetime.now()
            
            # Check if redirected to login page
            if 'login' in response.url.lower() or response.status_code in [401, 403]:
                print(f"⚠️  Session validation failed for {user_session.email}")
                user_session.validation_failures += 1
                
                if user_session.validation_failures >= 3:
                    self.invalidate_session(session_id, "Multiple validation failures")
                
                return False
            
            # Session is valid
            user_session.last_validated = datetime.now()
            user_session.validation_failures = 0
            return True
            
        except Exception as e:
            print(f"❌ Validation error for {user_session.email}: {e}")
            user_session.validation_failures += 1
            return False
    
    def invalidate_session(self, session_id: str, reason: str = "Unknown"):
        """Mark a session as invalidated and send alert."""
        if session_id not in self.sessions:
            return
        
        user_session = self.sessions[session_id]
        user_session.is_authenticated = False
        
        alert = {
            'timestamp': datetime.now(),
            'session_id': session_id,
            'email': user_session.email,
            'reason': reason,
            'duration': datetime.now() - user_session.login_time if user_session.login_time else None
        }
        
        self.alerts.append(alert)
        
        print(f"🚨 ALERT: Session invalidated for {user_session.email}")
        print(f"   Reason: {reason}")
        print(f"   Duration: {alert['duration']}")
        
    def get_next_active_session(self) -> Optional[str]:
        """Get the next active session using round-robin rotation."""
        active_sessions = [sid for sid, session in self.sessions.items() 
                          if session.is_authenticated]
        
        if not active_sessions:
            return None
        
        # Round-robin rotation
        if self.rotation_index >= len(active_sessions):
            self.rotation_index = 0
        
        selected_session = active_sessions[self.rotation_index]
        self.rotation_index += 1
        
        return selected_session
    
    def rotate_session(self) -> Optional[str]:
        """Rotate to the next active session."""
        next_session = self.get_next_active_session()
        
        if next_session:
            old_session = self.current_session_id
            self.current_session_id = next_session
            
            old_user = self.sessions[old_session].email if old_session else "None"
            new_user = self.sessions[next_session].email
            
            print(f"🔄 Rotated session: {old_user} → {new_user}")
            
        return next_session
    
    def monitor_sessions(self):
        """Background thread to monitor session validity."""
        print(f"👁️  Starting session monitoring (interval: {self.check_interval}s)")
        
        while self.monitoring_active:
            try:
                print(f"\n🔍 Monitoring check at {datetime.now().strftime('%H:%M:%S')}")
                
                # Check all sessions
                for session_id, user_session in self.sessions.items():
                    if user_session.is_authenticated:
                        is_valid = self.validate_session(session_id)
                        
                        if not is_valid and user_session.is_authenticated:
                            self.invalidate_session(session_id, "Session validation failed")
                
                # Print session status
                active_count = sum(1 for s in self.sessions.values() if s.is_authenticated)
                print(f"📊 Active sessions: {active_count}/{len(self.sessions)}")
                
                # Wait for next check
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(5)
    
    def start_monitoring(self):
        """Start background session monitoring."""
        if self.monitoring_active:
            print("⚠️  Monitoring already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self.monitor_sessions, daemon=True)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop background session monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        print("🛑 Session monitoring stopped")
    
    def make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """Make a request using the current active session with rotation."""
        if not self.current_session_id:
            self.current_session_id = self.get_next_active_session()
        
        if not self.current_session_id:
            print("❌ No active sessions available")
            return None
        
        user_session = self.sessions[self.current_session_id]
        
        try:
            if method.upper() == 'GET':
                response = user_session.session.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = user_session.session.post(url, **kwargs)
            else:
                print(f"❌ Unsupported method: {method}")
                return None
            
            # Update activity time
            user_session.last_activity = datetime.now()
            
            # Check if session is still valid
            if 'login' in response.url.lower():
                self.invalidate_session(self.current_session_id, "Redirected to login")
                # Try to rotate to another session
                self.rotate_session()
                return None
            
            return response
            
        except Exception as e:
            print(f"❌ Request error with session {user_session.email}: {e}")
            return None
    
    def get_session_stats(self) -> Dict:
        """Get comprehensive session statistics."""
        now = datetime.now()
        
        stats = {
            'total_sessions': len(self.sessions),
            'active_sessions': sum(1 for s in self.sessions.values() if s.is_authenticated),
            'inactive_sessions': sum(1 for s in self.sessions.values() if not s.is_authenticated),
            'total_alerts': len(self.alerts),
            'recent_alerts': len([a for a in self.alerts if now - a['timestamp'] < timedelta(hours=1)]),
            'sessions': {}
        }
        
        for session_id, user_session in self.sessions.items():
            session_stats = {
                'email': user_session.email,
                'is_authenticated': user_session.is_authenticated,
                'login_time': user_session.login_time,
                'last_validated': user_session.last_validated,
                'last_activity': user_session.last_activity,
                'validation_failures': user_session.validation_failures,
                'session_duration': now - user_session.login_time if user_session.login_time else None
            }
            stats['sessions'][session_id] = session_stats
        
        return stats
    
    def print_status(self):
        """Print current status of all sessions."""
        print("\n📊 Session Manager Status:")
        print("=" * 60)
        
        stats = self.get_session_stats()
        
        print(f"Total Sessions: {stats['total_sessions']}")
        print(f"Active Sessions: {stats['active_sessions']}")
        print(f"Inactive Sessions: {stats['inactive_sessions']}")
        print(f"Total Alerts: {stats['total_alerts']}")
        print(f"Recent Alerts: {stats['recent_alerts']}")
        
        if self.current_session_id:
            current_user = self.sessions[self.current_session_id].email
            print(f"Current Session: {current_user}")
        
        print("\n📋 Session Details:")
        print("-" * 60)
        
        for session_id, user_session in self.sessions.items():
            status = "🟢 Active" if user_session.is_authenticated else "🔴 Inactive"
            duration = ""
            
            if user_session.login_time:
                duration = datetime.now() - user_session.login_time
                duration = f" ({duration})"
            
            print(f"{status} {user_session.email}{duration}")
            
            if user_session.last_validated:
                print(f"   Last validated: {user_session.last_validated.strftime('%H:%M:%S')}")
            
            if user_session.validation_failures > 0:
                print(f"   Validation failures: {user_session.validation_failures}")
        
        if self.alerts:
            print("\n🚨 Recent Alerts:")
            print("-" * 60)
            for alert in self.alerts[-3:]:  # Show last 3 alerts
                print(f"{alert['timestamp'].strftime('%H:%M:%S')} - {alert['email']}: {alert['reason']}")


def main():
    """Main function to demonstrate the session manager."""
    print("🚀 LAB8 Bonus: Multi-Session Manager")
    print("=" * 60)
    
    # Configuration
    login_url = "https://www.scrapingcourse.com/login/csrf"
    protected_url = "https://www.scrapingcourse.com/ecommerce"
    
    # Create session manager
    manager = SessionManager(login_url, protected_url, check_interval=15)
    
    # Add multiple users (using placeholder credentials, will be detected automatically)
    users = [
        ("user1@example.com", "password"),
        ("user2@example.com", "password"),  
        ("user3@example.com", "password"),  
    ]
    
    print("👥 Adding user sessions...")
    session_ids = []
    for i, (email, password) in enumerate(users):
        # Create unique emails for demonstration
        unique_email = f"session{i+1}@example.com"
        session_id = manager.add_user(unique_email, password)
        session_ids.append(session_id)
    
    print(f"\n🔐 Logging in {len(session_ids)} users...")
    
    # Login all users
    login_results = []
    for session_id in session_ids:
        success = manager.login_user(session_id)
        login_results.append(success)
        time.sleep(1)  # Small delay between logins
    
    successful_logins = sum(login_results)
    print(f"✅ Successfully logged in {successful_logins}/{len(session_ids)} users")
    
    if successful_logins == 0:
        print("❌ No successful logins. Exiting...")
        return
    
    # Start monitoring
    manager.start_monitoring()
    
    # Print initial status
    manager.print_status()
    
    print("\n🔄 Testing session rotation and requests...")
    
    # Simulate activity with session rotation
    for i in range(5):  # Reduced to 5 requests
        print(f"\n--- Request {i+1} ---")
        
        # Make a request
        response = manager.make_request(protected_url)
        
        if response:
            print(f"✅ Request successful (Status: {response.status_code})")
            
            # Extract some content
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"   Page title: {title.get_text().strip()}")
        else:
            print("❌ Request failed")
        
        # Rotate to next session
        manager.rotate_session()
        
        # Wait a bit
        time.sleep(2)
    
    print("\n🧪 Testing session invalidation...")
    
    # Simulate session invalidation by modifying cookies
    if manager.current_session_id:
        current_session = manager.sessions[manager.current_session_id]
        
        # Modify a cookie to invalidate session
        for cookie in current_session.session.cookies:
            if 'session' in cookie.name.lower() or 'auth' in cookie.name.lower():
                current_session.session.cookies.set(
                    cookie.name, 
                    cookie.value + "_invalid",
                    domain=cookie.domain,
                    path=cookie.path
                )
                print(f"🔧 Modified cookie: {cookie.name}")
                break
        
        # Make a request to trigger invalidation
        print("Testing access with modified cookie...")
        response = manager.make_request(protected_url)
        
        if not response:
            print("✅ Session invalidation detected correctly")
    
    # Wait for monitoring to run a few cycles (reduced time)
    print(f"\n⏰ Monitoring sessions for 20 seconds...")
    time.sleep(20)
    
    # Print final status
    manager.print_status()
    
    # Stop monitoring
    manager.stop_monitoring()
    
    # Print session statistics
    stats = manager.get_session_stats()
    
    print("\n📈 Final Statistics:")
    print("=" * 50)
    print(f"Total Sessions Created: {stats['total_sessions']}")
    print(f"Currently Active: {stats['active_sessions']}")
    print(f"Total Alerts Generated: {stats['total_alerts']}")
    
    if manager.alerts:
        print(f"\n🚨 Alert Summary:")
        for alert in manager.alerts:
            print(f"  - {alert['email']}: {alert['reason']} at {alert['timestamp'].strftime('%H:%M:%S')}")
    
    print("\n🎉 Multi-session management demonstration completed!")


if __name__ == "__main__":
    main() 