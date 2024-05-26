#!/bin/env bash

# Install Nginx if it is not already installed
if ! which nginx > /dev/null; then
    echo "Nginx is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y nginx
else
    echo "Nginx is already installed."
fi

# Create the required directories
directories=(
    "/data"
    "/data/web_static"
    "/data/web_static/releases"
    "/data/web_static/shared"
    "/data/web_static/releases/test"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "Creating directory $dir..."
        sudo mkdir -p "$dir"
    else
        echo "Directory $dir already exists."
    fi
done

# Create a fake HTML file
echo "Creating fake HTML file..."
echo "<html>
  <head>
  </head>
  <body>
    Welcome to techpackets.tech
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create (or recreate) the symbolic link
if [ -L "/data/web_static/current" ]; then
    echo "Removing existing symbolic link..."
    sudo rm -f /data/web_static/current
fi
echo "Creating new symbolic link..."
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group
echo "Changing ownership of /data/ to ubuntu user and group..."
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
echo "Updating Nginx configuration..."
sudo sed -i '/^\tlocation \/ {/i \ \tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
echo "Restarting Nginx..."
sudo service nginx restart

echo "Setup completed successfully."
