# hp-envy-27-hdmi-in
Scripts to enable HDMI input switching on the HP Envy 27

Put both service files in /etc/systemd/system

Run: sudo systemctl daemon-reload

Copy the python file to /opt/bin

Run:

sudo systemctl enable hdmi-input-toggle.service
sudo systemctl enable setkeycodes.service 
sudo systemctl start hdmi-input-toggle.service
sudo systemctl start setkeycodes.service 


Now the button under the left corner of the display should toggle between the internal display adapter and the HDMI port
