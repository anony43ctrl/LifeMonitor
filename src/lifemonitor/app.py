import os
import sys
import socketserver
import time
import threading
import asyncio
import json
import logging
from pathlib import Path
from wsgiref.simple_server import WSGIServer
from urllib.parse import parse_qs
from urllib.request import urlopen
from urllib.error import URLError

import django
from django.core.handlers.wsgi import WSGIHandler
from django.core.servers.basehttp import WSGIRequestHandler
from django.core.management import call_command

import toga

# --- LOGGING SETUP ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LifeMonitor")

# Placeholder variables for Android classes
Environment = None
Intent = None
Settings = None
Uri = None
Build = None

class ThreadedWSGIServer(socketserver.ThreadingMixIn, WSGIServer):
    """Handle requests in a separate thread."""
    pass

class Lifemonitor(toga.App):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server_mode = "SETUP" # Options: SETUP, LOADING, DJANGO
        self.django_app = None
        self.setup_error = None
        self._httpd = None

    # --- 1. THE MASTER REQUEST HANDLER ---
    def master_wsgi_handler(self, environ, start_response):
        """
        Decides what to show based on the current state of the app.
        This runs inside the server thread for every request.
        """
        path = environ.get('PATH_INFO', '/')
        
        # A. SETUP MODE
        if self.server_mode == "SETUP":
            return self.handle_setup_requests(environ, start_response)
        
        # B. LOADING MODE
        elif self.server_mode == "LOADING":
            return self.serve_html(start_response, self.get_loading_html())
        
        # C. DJANGO MODE
        elif self.server_mode == "DJANGO":
            if self.django_app:
                return self.django_app(environ, start_response)
            else:
                # Fallback if Django crashed or isn't ready yet
                return self.serve_html(start_response, self.get_loading_html())
        
        return [b"Unknown State"]

    # --- 2. SETUP REQUEST LOGIC ---
    def handle_setup_requests(self, environ, start_response):
        query = parse_qs(environ.get('QUERY_STRING', ''))
        
        # User clicked a button (detected via URL params)
        mode_list = query.get('mode')
        
        if mode_list:
            mode = mode_list[0]
            if mode == 'private':
                self.trigger_setup_completion('private')
                return self.redirect_home(start_response)
            
            elif mode == 'public':
                # We must verify permissions on the MAIN thread
                has_perm = self.verify_storage_permissions_blocking()
                if has_perm:
                    self.trigger_setup_completion('public')
                    return self.redirect_home(start_response)
                else:
                    # Show permission instructions
                    return self.serve_html(start_response, self.get_permission_html())

        # Default: Show Setup Screen
        return self.serve_html(start_response, self.get_setup_html())

    def serve_html(self, start_response, html):
        start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
        return [html.encode('utf-8')]

    def redirect_home(self, start_response):
        # Redirect back to root to clear query params
        start_response('302 Found', [('Location', '/')])
        return [b'Redirecting...']

    def trigger_setup_completion(self, mode):
        """Save config and start Django loading process."""
        logger.info(f"UI: Setup completed. Mode: {mode}")
        
        # 1. Configure Storage
        self.configure_android_storage(mode)

        # 2. Save Config
        try:
            config_path = self.paths.data / "storage_config.json"
            with open(config_path, 'w') as f:
                json.dump({"storage_mode": mode}, f)
        except Exception as e:
            logger.error(f"Config Save Failed: {e}")
        
        # 3. Switch UI to Loading and Start Django
        self.server_mode = "LOADING"
        
        # [FIX] Use URL reassignment instead of .reload()
        self.loop.call_soon_threadsafe(self.refresh_webview)
        
        threading.Thread(target=self.init_django, daemon=True).start()

    def refresh_webview(self):
        """Helper to safely refresh the page on the main thread."""
        try:
            # Re-setting the URL forces a reload
            self.web_view.url = self.local_url
        except Exception as e:
            logger.error(f"WebView Refresh Error: {e}")

    # --- 3. DJANGO INITIALIZATION ---
    def init_django(self):
        logger.info("Background: Starting Django Init...")
        try:
            # Setup
            django.setup(set_prefix=False)
            
            # Migrate
            logger.info("Background: Running Migrations...")
            call_command("migrate", interactive=False)
            
            # Ready
            self.django_app = WSGIHandler()
            self.server_mode = "DJANGO"
            logger.info("Background: Django Ready! Switched mode.")
            
            # [FIX] Use URL reassignment instead of .reload()
            self.loop.call_soon_threadsafe(self.refresh_webview)
            
        except Exception as e:
            logger.error(f"Django Init Error: {e}", exc_info=True)
            self.server_mode = "ERROR" 

    # --- 4. SYSTEM & ANDROID HELPERS ---
    def verify_storage_permissions_blocking(self):
        """Checks permissions. If missing, launches settings UI."""
        if sys.platform != "android": return True
        
        try:
            # Run on main thread via Future
            future = asyncio.run_coroutine_threadsafe(self._check_perm_ui(), self.loop)
            return future.result()
        except Exception as e:
            logger.error(f"Perm Check Failed: {e}")
            return False

    async def _check_perm_ui(self):
        """Actual Android API call on Main Thread"""
        try:
            from java import jclass
            Environment = jclass("android.os.Environment")
            Intent = jclass("android.content.Intent")
            Settings = jclass("android.provider.Settings")
            Uri = jclass("android.net.Uri")
            Build = jclass("android.os.Build")

            if Build.VERSION.SDK_INT >= 30:
                if not Environment.isExternalStorageManager():
                    logger.info("UI: Launching Permission Settings...")
                    intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
                    package_uri = Uri.parse("package:" + self._impl.native.getPackageName())
                    intent.setData(package_uri)
                    self._impl.native.startActivity(intent)
                    return False
            return True
        except Exception as e:
            logger.error(f"Android API Error: {e}")
            return True

    def configure_android_storage(self, mode):
        if sys.platform != "android":
            os.environ["ANDROID_DATA_PATH"] = str(self.paths.data)
            return

        try:
            from java import jclass
            Environment = jclass("android.os.Environment")
            
            if mode == "public":
                docs = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOCUMENTS).getAbsolutePath()
                path = os.path.join(str(docs), "LifeMonitor")
            else:
                path = str(self.paths.data / "data")

            if not os.path.exists(path):
                os.makedirs(path, exist_ok=True)
            
            os.environ["ANDROID_DATA_PATH"] = path
            logger.info(f"Storage Path Set: {path}")
            
        except Exception as e:
            logger.error(f"Storage Config Error: {e}")
            os.environ["ANDROID_DATA_PATH"] = str(self.paths.data)

    def handle_back_button(self, app, **kwargs):
        try:
            self.web_view.evaluate_javascript("history.back()")
        except: pass
        return False

    # --- 5. APP STARTUP ---
    def startup(self):
        # A. Configure Python Path
        webapp_path = Path(__file__).parent.parent / "webapp"
        sys.path.append(str(webapp_path))
        os.environ["DJANGO_SETTINGS_MODULE"] = "user_monitoring.settings"

        # B. Determine Initial State
        config_path = self.paths.data / "storage_config.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    mode = json.load(f).get("storage_mode", "private")
                self.configure_android_storage(mode)
                self.server_mode = "LOADING"
                # Start Django Init in background
                threading.Thread(target=self.init_django, daemon=True).start()
            except:
                self.server_mode = "SETUP"
        else:
            self.server_mode = "SETUP"

        # C. Start Server
        self._httpd = ThreadedWSGIServer(("127.0.0.1", 0), WSGIRequestHandler)
        self._httpd.daemon_threads = True
        
        # Set our app logic
        self._httpd.set_app(self.master_wsgi_handler)
        
        # Get Port
        host, port = self._httpd.socket.getsockname()
        self.local_url = f"http://{host}:{port}/"
        logger.info(f"Server running at {self.local_url}")
        
        # Run Server
        threading.Thread(target=self._httpd.serve_forever, daemon=True).start()

        # D. Setup GUI
        self.web_view = toga.WebView()
        self.web_view.url = self.local_url # Load localhost immediately
        
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.web_view
        self.on_exit = self.handle_back_button
        self.main_window.show()

        # Hide Action Bar
        try:
            if hasattr(self, "_impl") and hasattr(self._impl, "native"):
                act = self._impl.native
                if hasattr(act, "getSupportActionBar") and act.getSupportActionBar():
                    act.getSupportActionBar().hide()
        except: pass

    # --- HTML TEMPLATES ---
    def get_loading_html(self):
        return """<!DOCTYPE html><html><body style="display:flex;justify-content:center;align-items:center;height:100vh;margin:0;">
        <div style="text-align:center;font-family:sans-serif;">
            <div style="width:50px;height:50px;border:5px solid #eee;border-top:5px solid #007AFF;border-radius:50%;animation:s 1s infinite linear;margin:0 auto 20px;"></div>
            <h2>Starting LifeMonitor...</h2>
            <p style="color:#888;">Initializing Database...</p>
        </div><style>@keyframes s{to{transform:rotate(360deg)}}</style>
        <script>
            // Auto-reload until Django takes over
            setTimeout(function(){ window.location.reload(); }, 2500);
        </script>
        </body></html>"""

    def get_permission_html(self):
        return """<!DOCTYPE html><html><body style="font-family:-apple-system,sans-serif;padding:40px;text-align:center;">
        <h2 style="color:#007AFF;">Permission Required</h2>
        <p>To save data in "Shared Documents", Android requires special access.</p>
        <p>We have opened the Settings page.</p>
        <ol style="text-align:left;display:inline-block;">
            <li>Find <b>LifeMonitor</b></li>
            <li>Turn <b>ON</b> "Allow access to all files"</li>
            <li>Press Back to return here</li>
        </ol>
        <br><br>
        <a href="/?mode=public" style="background:#007AFF;color:white;padding:15px 30px;text-decoration:none;border-radius:12px;font-weight:bold;">I Have Enabled It</a>
        <br><br><a href="/" style="color:#888;">Cancel</a>
        </body></html>"""

    def get_setup_html(self):
        return """<!DOCTYPE html><html lang="en"><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: -apple-system, sans-serif; background: #F2F2F7; padding: 20px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
            .card { background: white; border-radius: 18px; padding: 24px; margin-bottom: 20px; width: 100%; max-width: 400px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); cursor: pointer; text-decoration: none; color: black; display: block; }
            .card:active { transform: scale(0.98); }
            h3 { margin: 0 0 5px 0; } p { margin: 0; color: #8E8E93; font-size: 14px; }
            .badge { display: inline-block; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; }
        </style></head><body>
            <h1 style="margin-bottom: 30px;">Where to save data?</h1>
            
            <a href="/?mode=private" class="card">
                <span class="badge" style="background:rgba(142,142,147,0.2);color:#3A3A3C;">Private</span>
                <h3>Internal Storage</h3>
                <p>Secure. Stored inside the app. Best if you don't plan to move files manually.</p>
            </a>

            <a href="/?mode=public" class="card">
                <span class="badge" style="background:rgba(0,122,255,0.15);color:#007AFF;">Shared</span>
                <h3>Documents Folder</h3>
                <p>Accessible. Saved as 'LifeMonitor' in Documents. Easy to backup.</p>
            </a>
        </body></html>"""

def main():
    return Lifemonitor()