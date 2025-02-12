In "command prompt" type: pip instal selenium ; pip instal flask

Since you have your own website, you need to host your Flask app on your server and connect it to your domain. Here’s how you can do it:
------------------------------------------------------------------------------------------------------------------------------------------
1. Check Your Hosting Type
Shared Hosting (cPanel-based)?
Most shared hosting does not support Flask. You may need a VPS.
VPS or Dedicated Server (Linux, Apache/Nginx)?
You can install Python and run Flask directly.
------------------------------------------------------------------------------------------------------------------------------------------
2. Upload Your Flask App to Your Server
------------------------------------------------------------------------------------------------------------------------------------------
A. If You Have cPanel (Shared Hosting)

1.Check if cPanel supports Python Apps:
  Log in to cPanel → Go to Setup Python App
  If not available, you may need a VPS.

2. Upload Your Flask App Files
  Use File Manager or FTP (FileZilla)
  Place your files in the public_html directory or a subfolder.

3. Set Up a Python Environment in cPanel
  Go to Setup Python App 
  Choose Python 3.x
  Set app.py as the entry point.

4. Install Dependencies
  In cPanel Terminal (or SSH):  pip install flask selenium gunicorn

5. Run Your Flask App
  In Setup Python App, click Start App.
----------------------------------------------------------------------------------------------------------------------------------------
B. If You Have a VPS (Linux Server)

1. Connect to Your Server Using SSH : ssh user@your-server-ip

2. Install Python & Flask:  sudo apt update && sudo apt install python3 python3-pip
                         pip3 install flask selenium gunicorn

3. Upload Your Flask App
Use FTP (FileZilla)
Or Git (if available):  git clone https://github.com/your-repo.git
                        cd your-repo 

4. Run the Flask App with Gunicorn:  gunicorn -w 4 -b 0.0.0.0:8000 app:app

5. Set Up a Web Server (Nginx or Apache)
For Nginx, add this to /etc/nginx/sites-available/default:
server {
    listen 80;
    server_name yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

6. Restart Nginx:  sudo systemctl restart nginx
------------------------------------------------------------------------------------------------------------------------------------------
3. Point Your Domain to Your Server

Go to your domain registrar
Update the A Record to point to your server’s IP.
Wait for DNS propagation (can take up to 24 hours).


