import socket
import numpy as np
import pickle

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('', ))  # Connect to the server at ('server IP address', port)

    print("Client connecté au serveur.")

    data_size = int.from_bytes(client_socket.recv(4), byteorder='big')

    data = bytearray()
    while len(data) < data_size:
        packet = client_socket.recv(4096)
        if not packet:
            break
        data.extend(packet)

    print("Matrices reçues. Déballage des données.")

    try:
        matrix, matrix1, matrix2 = pickle.loads(data)
        print("Matrice reçue :")
        print(matrix)
        print("Matrice 2 reçue :")
        print(matrix2)
    except Exception as e:
        print(f"Erreur lors du déballage des données : {e}")

    try:
        result = np.dot(matrix, matrix2)
        print("Résultat du produit de la grande matrice et matrix2 :")
        print(result)
    except Exception as e:
        print(f"Erreur lors du calcul du produit matriciel : {e}")

    try:
        serialized_result = pickle.dumps(result)
        result_size = len(serialized_result)
        client_socket.sendall(result_size.to_bytes(4, byteorder='big'))
        client_socket.sendall(serialized_result)
        print("Résultat envoyé au serveur.")
    except Exception as e:
        print(f"Erreur lors de l'envoi des données : {e}")

    client_socket.close()
    print("Connexion fermée.")

if __name__ == "__main__":
    main()
