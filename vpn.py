from wireguard import Server

server = Server('IP:PORT', 'IP', address='DNS(LOCAL_IP)')

def vpn():
  # Write out the server config to the default location: /etc/wireguard/wg0.conf
  server.config().write()