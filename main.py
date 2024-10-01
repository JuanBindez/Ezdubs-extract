import requests
import re
import sys

# Função para baixar o arquivo de áudio
def download_audio(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Levanta um erro para respostas ruins
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f'Áudio baixado como {filename}')
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao baixar o áudio: {e}")

# Função para extrair e baixar o áudio
def extract_and_download_audio(page_url):
    try:
        # Obtém o conteúdo HTML da página
        response = requests.get(page_url)
        response.raise_for_status()  # Levanta um erro para respostas ruins
        
        # Procura pela URL do áudio usando regex
        pattern = r'let dubbedAudioURL = "(.*?)";'
        match = re.search(pattern, response.text)
        
        if match:
            audio_url = match.group(1)
            print(f"URL do áudio encontrada: {audio_url}")
            
            # Baixa o arquivo de áudio
            download_audio(audio_url, 'downloaded_audio.mp3')
        else:
            print("Nenhuma URL de áudio encontrada na variável 'dubbedAudioURL'.")
    except requests.exceptions.RequestException as e:
        print(f"Ocorreu um erro ao acessar a página: {e}")

# Bloco principal para lidar com o argumento da linha de comando
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python script.py <URL>")
        sys.exit(1)
    
    # Obtém a URL a partir do argumento da linha de comando
    page_url = sys.argv[1]
    
    # Chama a função para extrair e baixar o áudio
    extract_and_download_audio(page_url)
