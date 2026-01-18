import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sqlite3

# ==================== EMAIL CONFIGURATION ====================
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "santhyalogu2006@gmail.com"  # Your Gmail
SENDER_PASSWORD = "qpim widd xyyc hyry"  # Gmail App Password (not regular password!)
ADMIN_EMAIL = "contactsaravanamedicals@gmail.com"  # Admin's email to receive alerts

DB_PATH = 'database/pharmacy.db'

def send_email(to_email, subject, html_content):
    """Send HTML email using Gmail SMTP"""
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Saravana Medicals <{SENDER_EMAIL}>"
        message["To"] = to_email
        
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {str(e)}")
        return False

def generate_expiry_email_html(near_expiry_medicines, expired_medicines):
    """Generate email with YOUR EXACT THEME COLORS"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 650px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #a8d8ff 0%, #b8e6e6 100%);
                color: #333;
                padding: 40px 30px;
                text-align: center;
                position: relative;
            }}
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
                background-size: 30px 30px;
            }}
            .header-content {{
                position: relative;
                z-index: 1;
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                font-size: 28px;
                font-weight: 600;
                color: #0093E9;
            }}
            .header p {{
                margin: 0;
                font-size: 14px;
                color: #666;
            }}
            .content {{
                padding: 30px;
            }}
            .alert-box {{
                background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(249, 115, 22, 0.1));
                border-left: 4px solid #f59e0b;
                padding: 20px;
                margin-bottom: 25px;
                border-radius: 8px;
            }}
            .alert-box.danger {{
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                border-left-color: #ef4444;
            }}
            .alert-box h2 {{
                margin: 0 0 10px 0;
                font-size: 20px;
                font-weight: 600;
            }}
            .alert-box.danger h2 {{
                color: #ef4444;
            }}
            .alert-box:not(.danger) h2 {{
                color: #f59e0b;
            }}
            .alert-box p {{
                margin: 0;
                font-size: 13px;
                color: #666;
            }}
            .medicine-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            .medicine-table th {{
                background: linear-gradient(135deg, rgba(0, 147, 233, 0.1) 0%, rgba(128, 208, 199, 0.1) 100%);
                padding: 12px;
                text-align: left;
                border-bottom: 2px solid #a8d8ff;
                font-size: 12px;
                color: #0093E9;
                font-weight: 600;
            }}
            .medicine-table td {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;
                color: #333;
            }}
            .medicine-table tr:hover {{
                background: #f8f9fa;
            }}
            .badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
            }}
            .badge-warning {{
                background: linear-gradient(135deg, #f59e0b, #f97316);
                color: white;
            }}
            .badge-danger {{
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
            }}
            .action-section {{
                margin-top: 30px;
                padding-top: 25px;
                border-top: 2px solid #f0f0f0;
                text-align: center;
            }}
            .action-section p {{
                font-size: 13px;
                color: #666;
                margin-bottom: 15px;
            }}
            .btn {{
                display: inline-block;
                padding: 14px 30px;
                background: linear-gradient(135deg, #0093E9 0%, #80D0C7 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 500;
                box-shadow: 0 4px 15px rgba(0, 147, 233, 0.3);
            }}
            .footer {{
                background: linear-gradient(135deg, #f5f7fa 0%, #e0e7ef 100%);
                padding: 25px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .footer strong {{
                color: #0093E9;
                font-size: 14px;
            }}
            .success-box {{
                text-align: center;
                padding: 50px 30px;
            }}
            .success-box h2 {{
                color: #10b981;
                font-size: 24px;
                margin-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-content">
                    <h1>🏥 Saravana Medicals</h1>
                    <p>Expiry Alert Notification</p>
                    <p style="margin-top: 10px; opacity: 0.8;">
                        {datetime.now().strftime('%B %d, %Y - %I:%M %p')}
                    </p>
                </div>
            </div>
            
            <div class="content">
    """
    
    # Near Expiry Section
    if near_expiry_medicines:
        html += f"""
                <div class="alert-box">
                    <h2>⚠️ Medicines Expiring Soon ({len(near_expiry_medicines)})</h2>
                    <p>The following medicines will expire within 30 days:</p>
                </div>
                
                <table class="medicine-table">
                    <thead>
                        <tr>
                            <th>Medicine Name</th>
                            <th>Batch</th>
                            <th>Expiry Date</th>
                            <th>Qty</th>
                            <th>Days Left</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for med in near_expiry_medicines:
            expiry = datetime.strptime(med['expiry_date'], '%Y-%m-%d')
            days_left = (expiry - datetime.now()).days
            
            html += f"""
                        <tr>
                            <td><strong>{med['medicine_name']}</strong></td>
                            <td>{med['batch_number']}</td>
                            <td>{med['expiry_date']}</td>
                            <td>{med['quantity']}</td>
                            <td><span class="badge badge-warning">{days_left} days</span></td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
        """
    
    # Expired Section
    if expired_medicines:
        html += f"""
                <div class="alert-box danger" style="margin-top: 30px;">
                    <h2>🚫 EXPIRED Medicines ({len(expired_medicines)})</h2>
                    <p><strong>URGENT:</strong> Remove these medicines from inventory immediately!</p>
                </div>
                
                <table class="medicine-table">
                    <thead>
                        <tr>
                            <th>Medicine Name</th>
                            <th>Batch</th>
                            <th>Expired On</th>
                            <th>Qty</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for med in expired_medicines:
            html += f"""
                        <tr>
                            <td><strong>{med['medicine_name']}</strong></td>
                            <td>{med['batch_number']}</td>
                            <td>{med['expiry_date']}</td>
                            <td>{med['quantity']}</td>
                            <td><span class="badge badge-danger">EXPIRED</span></td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
        """
    
    # No alerts
    if not near_expiry_medicines and not expired_medicines:
        html += """
                <div class="success-box">
                    <h2>✅ All Good!</h2>
                    <p style="color: #666;">No medicines are expiring or expired at this time.</p>
                </div>
        """
    
    # Footer
    html += f"""
                <div class="action-section">
                    <p><strong>Action Required:</strong> Please review and take necessary action.</p>
                    <a href="http://127.0.0.1:5000/expiry" class="btn">
                        View in System →
                    </a>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Saravana Medicals</strong></p>
                <p style="margin: 5px 0;">Pharmacy Inventory Management System</p>
                <p style="margin-top: 10px; font-size: 11px; opacity: 0.7;">
                    This is an automated alert. Please do not reply to this email.
                </p>
                <p style="margin-top: 15px; font-size: 11px;">
                    © {datetime.now().year} Saravana Medicals. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def check_and_send_expiry_alerts():
    """Check database and send email alerts"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Near expiry (next 30 days)
        near_expiry = cursor.execute('''
            SELECT medicine_name, batch_number, expiry_date, quantity
            FROM medicines
            WHERE DATE(expiry_date) BETWEEN DATE('now') AND DATE('now', '+30 days')
            AND quantity > 0
            ORDER BY expiry_date
        ''').fetchall()
        
        # Expired medicines
        expired = cursor.execute('''
            SELECT medicine_name, batch_number, expiry_date, quantity
            FROM medicines
            WHERE DATE(expiry_date) < DATE('now')
            AND quantity > 0
            ORDER BY expiry_date DESC
        ''').fetchall()
        
        conn.close()
        
        near_expiry_list = [dict(row) for row in near_expiry]
        expired_list = [dict(row) for row in expired]
        
        if near_expiry_list or expired_list:
            subject = f"⚠️ Saravana Medicals Alert: {len(expired_list)} Expired, {len(near_expiry_list)} Expiring Soon"
            html_content = generate_expiry_email_html(near_expiry_list, expired_list)
            
            success = send_email(ADMIN_EMAIL, subject, html_content)
            
            if success:
                print(f"✅ Alert sent! Expired: {len(expired_list)}, Near Expiry: {len(near_expiry_list)}")
            
            return success
        else:
            print("✅ No expiry alerts needed!")
            return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def send_low_stock_alert(low_stock_medicines):
    """
    Send email alert for low stock medicines
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 650px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
                color: white;
                padding: 40px 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0 0 10px 0;
                font-size: 28px;
                font-weight: 600;
            }}
            .content {{
                padding: 30px;
            }}
            .alert-box {{
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                border-left: 4px solid #ef4444;
                padding: 20px;
                margin-bottom: 25px;
                border-radius: 8px;
            }}
            .alert-box h2 {{
                margin: 0 0 10px 0;
                font-size: 20px;
                font-weight: 600;
                color: #ef4444;
            }}
            .medicine-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}
            .medicine-table th {{
                background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
                padding: 12px;
                text-align: left;
                border-bottom: 2px solid #fecaca;
                font-size: 12px;
                color: #ef4444;
                font-weight: 600;
            }}
            .medicine-table td {{
                padding: 12px;
                border-bottom: 1px solid #f0f0f0;
                font-size: 13px;
            }}
            .badge {{
                display: inline-block;
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 11px;
                font-weight: 600;
                background: linear-gradient(135deg, #ef4444, #dc2626);
                color: white;
            }}
            .btn {{
                display: inline-block;
                padding: 14px 30px;
                background: linear-gradient(135deg, #0093E9 0%, #80D0C7 100%);
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 500;
            }}
            .footer {{
                background: #f5f7fa;
                padding: 25px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚨 LOW STOCK ALERT</h1>
                <p>Saravana Medicals - Stock Monitoring</p>
                <p style="margin-top: 10px; opacity: 0.9;">
                    {datetime.now().strftime('%B %d, %Y - %I:%M %p')}
                </p>
            </div>
            
            <div class="content">
                <div class="alert-box">
                    <h2>⚠️ {len(low_stock_medicines)} Medicine(s) Below Minimum Stock Level</h2>
                    <p>The following medicines have stock quantity less than 5 units. Immediate reordering recommended!</p>
                </div>
                
                <table class="medicine-table">
                    <thead>
                        <tr>
                            <th>Medicine Name</th>
                            <th>Category</th>
                            <th>Current Stock</th>
                            <th>Supplier</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for med in low_stock_medicines:
        html += f"""
                        <tr>
                            <td><strong>{med['medicine_name']}</strong></td>
                            <td>{med['category']}</td>
                            <td><strong style="color: #ef4444;">{med['quantity']} units</strong></td>
                            <td>{med.get('supplier_name', 'N/A')}</td>
                            <td><span class="badge">CRITICAL</span></td>
                        </tr>
        """
    
    html += f"""
                    </tbody>
                </table>
                
                <div style="margin-top: 30px; padding-top: 25px; border-top: 2px solid #f0f0f0; text-align: center;">
                    <p style="font-size: 13px; color: #666; margin-bottom: 15px;">
                        <strong>Action Required:</strong> Please create purchase orders for these medicines.
                    </p>
                    <a href="http://127.0.0.1:5000/stock" class="btn">
                        View Stock →
                    </a>
                </div>
            </div>
            
            <div class="footer">
                <p><strong>Saravana Medicals</strong></p>
                <p style="margin: 5px 0;">Automated Stock Monitoring System</p>
                <p style="margin-top: 15px; font-size: 11px;">
                    © {datetime.now().year} Saravana Medicals. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    subject = f"🚨 LOW STOCK ALERT: {len(low_stock_medicines)} Medicine(s) Need Reordering"
    return send_email(ADMIN_EMAIL, subject, html)


def check_low_stock_and_alert():
    """
    Check for medicines with quantity < 5 and send alert
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        
        low_stock = conn.execute('''
            SELECT m.medicine_name, m.category, m.quantity, s.supplier_name
            FROM medicines m
            LEFT JOIN suppliers s ON m.supplier_id = s.supplier_id
            WHERE m.quantity > 0 AND m.quantity < 5
            ORDER BY m.quantity ASC
        ''').fetchall()
        
        conn.close()
        
        if low_stock:
            low_stock_list = [dict(row) for row in low_stock]
            success = send_low_stock_alert(low_stock_list)
            
            if success:
                print(f"✅ Low stock alert sent! {len(low_stock_list)} medicines below minimum.")
            return success
        else:
            print("✅ All medicines have sufficient stock.")
            return True
            
    except Exception as e:
        print(f"❌ Error checking low stock: {str(e)}")
        return False

def send_test_email():
    """Send test email"""
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
            }}
            .container {{
                max-width: 500px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 15px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                text-align: center;
            }}
            h2 {{
                background: linear-gradient(135deg, #0093E9 0%, #80D0C7 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 28px;
                margin-bottom: 20px;
            }}
            p {{
                color: #666;
                line-height: 1.6;
            }}
            .success-icon {{
                font-size: 60px;
                margin-bottom: 20px;
            }}
            .timestamp {{
                margin-top: 20px;
                padding-top: 20px;
                border-top: 2px solid #f0f0f0;
                font-size: 12px;
                color: #999;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success-icon">✅</div>
            <h2>Test Email Successful!</h2>
            <p>Your email configuration is working correctly.</p>
            <p><strong>Saravana Medicals</strong> is now ready to send expiry alerts.</p>
            <div class="timestamp">
                Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
    </body>
    </html>
    """
    
    return send_email(ADMIN_EMAIL, "🧪 Test Email - Saravana Medicals", html)