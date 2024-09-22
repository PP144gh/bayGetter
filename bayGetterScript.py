import requests
import subprocess
import socks
import socket

# Set up the SOCKS proxy to use Tor
socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
socket.socket = socks.socksocket

def getUrl():
    query = input('What would you like to torrent? ')
    return query

def search():
    query = getUrl()
    baseURL = 'https://apibay.org/q.php?q='
    url = baseURL + query

    print(f"Searching for torrents: {url}")

    try:
        # Make the request through the Tor network
        r = requests.get(url)
        r.raise_for_status()

        # Parse the JSON response from the API
        torrents = r.json()

        if torrents:
            # Display the first five torrents
            print("\nTop 5 search results:")
            top_torrents = torrents[:5]  # Get the first 5 torrents
            for idx, torrent in enumerate(top_torrents, start=1):
                name = torrent.get("name", "Unknown")
                size = torrent.get("size", "Unknown")
                seeders = torrent.get("seeders", "Unknown")
                print(f"{idx}. {name} | Size: {int(size)/(1024**3):.2f} GB | Seeders: {seeders}")

            # Ask the user to choose one of the torrents
            choice = int(input("\nEnter the number of the torrent you'd like to download (1-5): ")) - 1

            if 0 <= choice < len(top_torrents):
                selected_torrent = top_torrents[choice]
                magnet_link = f"magnet:?xt=urn:btih:{selected_torrent['info_hash']}"
                print(f"\nDownloading: {selected_torrent['name']}")
                print(f"Magnet Link: {magnet_link}")

                # Open the torrent client (Transmission in this case) with the magnet link
                subprocess.Popen(['transmission-gtk', magnet_link])
            else:
                print("Invalid selection. Please choose a number between 1 and 5.")
        else:
            print("No torrents found.")
    except requests.RequestException as e:
        print(f"Failed to retrieve search results: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Repeat the search
    search()

search()
