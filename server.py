import socket
import numpy as np
import pickle

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', ))  # Bind the server to ('server IP address', port)
    server_socket.listen(2)  

    print("Le serveur est en attente de connexion des noeuds...")

    connections = []
    for i in range(2):  
        conn, addr = server_socket.accept()
        print(f"Noeud {i+1} connecté depuis {addr}.")
        connections.append(conn)

    matrixA = np.random.randint(low=1, high=1000, size=(1000, 1000))
    matrixB = np.random.randint(low=1, high=1000, size=(1000, 1000))

    print("Matrix A:")
    print(matrixA)

    print("\nMatrix B:")
    print(matrixB)

    print("Matrice (avant extraction) :")
    print(matrixB)

    matrix1 = np.triu(matrixB)
    matrix2 = np.tril(matrixB)

    np.fill_diagonal(matrix1, 0)

    print("Matrice 1 (triangulaire supérieure) :")
    print(matrix1)
    print("Matrice 2 (triangulaire inférieure) :")
    print(matrix2)

    for i, conn in enumerate(connections):
        data = pickle.dumps((matrixA, matrix1, matrix2))
        data_size = len(data)
        conn.sendall(data_size.to_bytes(4, byteorder='big'))
        conn.sendall(data)
        print(f"Sous-matrice {i+1} envoyée au noeud {i+1}.")

    print("Sous-matrices envoyées. En attente des résultats...")

    received_matrices = []

    for i, conn in enumerate(connections):
        data_size = int.from_bytes(conn.recv(4), byteorder='big')
        data = bytearray()
        while len(data) < data_size:
            packet = conn.recv(4096)
            if not packet:
                break
            data.extend(packet)

        response = pickle.loads(data)
        print(f"Réponse du noeud {i+1} :")
        print(response)

        received_matrices.append(response)

    if len(received_matrices) == 2:
        summed_matrix = received_matrices[0] + received_matrices[1]
        print("Somme des matrices reçues :")
        print(summed_matrix)

    print("Toutes les réponses ont été reçues.")

    for conn in connections:
        conn.close()
    server_socket.close()

if __name__ == "__main__":
    main()
