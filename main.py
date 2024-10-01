import requests
import re
import sys

def download_audio(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f'Áudio baixado como {filename}')
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao baixar o áudio: {e}")

def extract_and_download_audio(page_url):
    try:
        response = requests.get(page_url)
        response.raise_for_status()
        
        pattern = r'let dubbedAudioURL = "(.*?)";'
        match = re.search(pattern, response.text)
        
        if match:
            audio_url = match.group(1)
            print(f"URL do áudio encontrada: {audio_url}")
            
            download_audio(audio_url, 'downloaded_audio.mp3')
        else:
            print("Nenhuma URL de áudio encontrada na variável 'dubbedAudioURL'.")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python script.py <URL>")
        sys.exit(1)
    
    page_url = sys.argv[1]
    
    extract_and_download_audio(page_url)
